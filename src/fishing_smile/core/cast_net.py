import logging
_logger = logging.getLogger(__name__)
from multiprocessing.pool import job_counter
import secrets
import smtplib
from email.message import Message
from email.mime.text import MIMEText
from collections.abc import Iterable

from sqlalchemy.dialects.mysql import insert
from sqlmodel import (
    Session,
    select,
)

from fishing_smile.settings import get_settings
from fishing_smile.core.model import *


settings = get_settings()


def register_target_profile(
    target: TargetProfile,
    session: Session,
    *,
    upsert: bool = True,
) -> TargetProfileTable:
    table = session.exec(
        select(TargetProfileTable).where(TargetProfileTable.email == target.email)
    ).first()
    if table:
        if upsert:
            for key, value in target.model_dump(exclude = ['id', 'email']).items():
                setattr(table, key, value)
        else:
            # TODO: Don't throw exception if there is no change
            raise Exception('Another target with the same email address already exist')
    else:
        table = TargetProfileTable(**target.model_dump(exclude = ['id']))

    session.add(table)
    return table


def register_new_attack(
    target: TargetProfile,
    scheme: AttackScheme,
    session: Session,
) -> AttackTable:
    ex_id = secrets.token_hex(16)  # token_urlsafe returns inconsistent string length
    target = register_target_profile(target, session)
    session.flush()
    attack = AttackTable(
        external_id = ex_id,
        scheme_name = scheme.name,
        target_id = target.id,
    )
    session.add(attack)
    return attack


def render_mail(
    target: TargetProfile,
    attack: Attack,
) -> Message:
    email_component = attack.scheme.components.first(kind = 'email')
    url = email_component.templates['url'].format(
        # FIXME: This can potentially leak sensitive settings to email.
        # Restrict what can be used as template variables.
        settings = settings,
        attack = attack,
    )
    subject = email_component.templates['subject'].format(
        attack = attack,
    )
    body = email_component.templates['body'].format(
        attack = attack,
        # TODO: Current templating language don't allow cross-referencing automatically yet.
        url = url,
    )

    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = settings.cast.sender
    msg['To'] = target.email
    return msg


def send_email(
    target: TargetProfile,
    attack: Attack,
) -> None:
    msg = render_mail(target, attack)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        with server.login(settings.cast.sender, settings.cast.password) as session:
            # TODO: Is `SMTP.send_message` a more appropriate choice?
            # https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.send_message
            session.sendmail(settings.cast.sender, target.email, msg.as_string())


def cast_net(
    targets: Iterable[TargetProfile],
    # TODO: Allow AttackScheme object for simplicity?
    scheme: AttackScheme | str,
    session: Session,
) -> None:
    if isinstance(scheme, str):
        scheme = AttackScheme.get(scheme)

    sent_count = 0
    for target in targets:
        attack = register_new_attack(target, scheme, session)
        session.commit()
        try:
            send_email(target, attack)
            sent_count += 1
        except:
            _logger.exception(f'Failed to send to {target.email}')
    _logger.info(f'Sent to {sent_count} email(s).')
