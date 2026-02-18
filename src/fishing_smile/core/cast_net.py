import logging
from multiprocessing.pool import job_counter

from fishing_smile.core.model import TargetProfileTable, AttackTable
from fishing_smile.database.engine import engine

_logger = logging.getLogger(__name__)
import secrets
import smtplib
from email.mime.text import MIMEText

from sqlmodel import (
    Session,
    select,
)

from fishing_smile.settings import get_settings

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


def update_database(target, scheme, session):
    ex_id = secrets.token_hex(16)  # token_urlsafe returns inconsistent string length
    if session.exec(select(TargetProfileTable).where(TargetProfileTable.email == target.email).exists()):
        updated_profile = TargetProfileTable(
            name=target.name,
            phone=target.phone,
            company=target.company,
            job_title=target.job_title,
        )
        session.add(updated_profile)
    else:
        new_profile = TargetProfileTable(
            name=target.name,
            email=target.email,
            phone=target.phone,
            company=target.company,
            job_title=target.job_title,
        )
        session.add(new_profile)
    t_id = session.exec(select(TargetProfileTable.id).where(TargetProfileTable.email == target.email))
    new_attack = AttackTable(
        external_id=ex_id,
        scheme_name=scheme,
        target_id=t_id,
    )
    session.add(new_attack)
    session.commit()
    return ex_id


def send_email(target, ex_id):
    with smtplib.SMTP("smtp.gmail.com", 587).starttls() as server:
        with server.login(settings.cast.sender, settings.cast.password) as session:
            msg = MIMEText(TEXT_MESSAGE.format(**target._asdict(), link=URL + ex_id, ), 'html')
            msg['Subject'] = SUBJECT
            msg['From'] = settings.cast.sender
            msg['To'] = target.email
            session.sendmail(settings.cast.sender, target.email, msg.as_string())


def cast_net(targets, scheme, session):
    sent_count = 0
    with Session(engine) as session:
        for target in targets:
            ex_id = update_database(target, scheme, session)
            try:
                send_email(target, ex_id)
                sent_count += 1
            except:
                _logger.exception(f'Failed to send to {target.email}')
        _logger.info(f'Sent to {sent_count} email(s).')
