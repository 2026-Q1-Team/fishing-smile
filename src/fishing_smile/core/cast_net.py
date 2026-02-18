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


# TODO -- change to modular email templates
URL = f"{settings.cast.url}/index.html?k="
SUBJECT = "Please change your Organization account password."
TEXT_MESSAGE = """Dear {name_en},
According to our new security policy, all Organization staff must change their password every 6 months.
Follow these steps below to change your Organization account password.
    Step 1. Go to <a href="{link}">this page</a>.
    Step 2. Enter your old password.
    Step 3. Enter your new password.
    Step 4. Confirm your new password.
    Step 5. Click "Submit".
Please be reminded that all staff must change their password before 28 Jan 2026. If your password is already expired please contact ICT support team.
*You will be automatically logged out of your account on all devices after this process.
**If you are not logged out automatically, please manually log out to allow the process to complete.

Thank you for taking your time to keep our organization secure.
- ICT Team.
"""


# TODO -- redesign the flow of cast_net
# Entire flow should probably be changed to avoid repeatedly connecting and disconnecting to the sql server.


def update_database(
    target: TargetProfile,
    scheme: str,
    session: Session,
):
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
        scheme_name = scheme,
        target_id = insert_result.inserted_primary_key[0],
    )
    session.add(new_attack)
    session.commit()
    return ex_id


def send_email(
    target: TargetProfile,
    ex_id: int,
):
    with smtplib.SMTP("smtp.gmail.com", 587).starttls() as server:
        with server.login(settings.cast.sender, settings.cast.password) as session:
            msg = MIMEText(TEXT_MESSAGE.format(**target.model_dump(), link=URL + ex_id, ), 'html')
            msg['Subject'] = SUBJECT
            msg['From'] = settings.cast.sender
            msg['To'] = target.email
            session.sendmail(settings.cast.sender, target.email, msg.as_string())


def cast_net(
    targets: Iterable[TargetProfile],
    # TODO: Might optionally allow AttackScheme object too
    scheme: str,
    session: Session,
):
    sent_count = 0
    for target in targets:
        ex_id = update_database(target, scheme, session)
        try:
            send_email(target, ex_id)
            sent_count += 1
        except:
            _logger.exception(f'Failed to send to {target.email}')
    _logger.info(f'Sent to {sent_count} email(s).')
