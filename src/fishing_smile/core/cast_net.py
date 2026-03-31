import logging
_logger = logging.getLogger(__name__)
from multiprocessing.pool import job_counter
import smtplib
from email.message import Message, EmailMessage
from collections.abc import Iterable

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
    target = register_target_profile(target, session)
    session.flush()
    attack = AttackTable(
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
    rendered = {}
    context = {
        # FIXME: This can potentially leak sensitive settings to email.
        # Restrict what can be used as template variables.
        'settings': settings,
        'attack': attack,
        'templates': rendered,
    }
    # TODO: Current templating language don't allow cross-referencing automatically yet.
    # We rely on rendering templates in the **correct** order and adding them to context
    for template_name in email_component.templates:
        rendered[template_name] = email_component.templates[template_name].jinja.render(**context)

    msg = EmailMessage()
    msg['Subject'] = rendered['subject']
    msg['From'] = settings.cast.sender
    msg['To'] = target.email
    # TODO -- make and run a test on this
    msg.set_content(rendered['body'], cte='7bit')  # this should be email body in plaintext only, can be preformatted, no images.
    try:
        msg.add_alternative(rendered['alt_body'])  # this should be email body in html only, can have image.
    except KeyError:
        _logger.info('email does not contain alt_body')
    return msg


def send_email(
    target: TargetProfile,
    attack: Attack,
) -> None:
    msg = render_mail(target, attack)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        with server.login(settings.cast.sender, settings.cast.password) as session:
            session.send_message(msg)


def cast_net(
    targets: Iterable[TargetProfile],
    # TODO: Allow AttackScheme object for simplicity?
    scheme: AttackScheme | str,
    session: Session,
) -> None:
    if isinstance(scheme, str):
        scheme = standard_schemes.get(scheme)

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
