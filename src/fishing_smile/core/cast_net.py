import logging
_logger = logging.getLogger(__name__)
from multiprocessing.pool import job_counter
import secrets
import smtplib
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


def update_database(
    target: TargetProfile,
    scheme: AttackScheme,
    session: Session,
) -> AttackTable:
    if not isinstance(target, TargetProfileTable):
        target = TargetProfileTable(**target.model_dump())

    ex_id = secrets.token_hex(16)  # token_urlsafe returns inconsistent string length
    insert_result = session.exec(
        insert(TargetProfileTable).values(
            **target.model_dump(exclude = ['id'])
        ).on_duplicate_key_update(
            **target.model_dump(exclude = ['id', 'email'])
        )
    )
    new_attack = AttackTable(
        external_id = ex_id,
        scheme_name = scheme.name,
        target_id = insert_result.inserted_primary_key[0],
    )
    session.add(new_attack)
    session.commit()
    # TODO: is this necessary?
    session.refresh(new_attack)
    return new_attack


def send_email(
    target: TargetProfile,
    attack: Attack,
) -> None:
    email_component = attack.scheme.components[0]
    assert email_component.kind == 'email', \
        'Assuming emailing is the first attack component right now. To be changed later.'
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
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        with server.login(settings.cast.sender, settings.cast.password) as session:
            msg = MIMEText(body, 'html')
            msg['Subject'] = subject
            msg['From'] = settings.cast.sender
            msg['To'] = target.email
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
        attack = update_database(target, scheme, session)
        try:
            send_email(target, attack)
            sent_count += 1
        except:
            _logger.exception(f'Failed to send to {target.email}')
    _logger.info(f'Sent to {sent_count} email(s).')
