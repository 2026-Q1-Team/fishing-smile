import logging
_logger = logging.getLogger(__name__)
import secrets
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText

import pymysql

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


def update_database(target, scheme):
    urc = secrets.token_hex(16)  # token_urlsafe returns inconsistent string length
    with pymysql.connect(**settings.db.model_dump()) as connection:
        with connection.cursor() as cursor:
            insert_profile = """
            IF NOT EXISTS (SELECT * FROM `Target Profile` WHERE `email` = %(email))
                INSERT INTO `Target Profile` (`name`, `email`, `phone`, `company`, `job_title`)
                VALUES (%(name)s, %(email)s, %(phone)s, %(company)s, %(job_title)s)
            ELSE
                UPDATE `Target Profile`
                SET (`name`, `phone`, `company`, `job_title`) = (%(name)s, %(phone)s, %(company)s, %(job_title)s)
                WHERE `email` = %(email)s
            """
            insert_attack = """
            INSERT INTO `Attack` (`external_id`, `scheme_name`, `target_id`)
            VALUES (%(urc)s, %(scheme)s, %(target.uid)s)
            """
            cursor.execute(insert_profile, (target,))
            cursor.execute(insert_attack,
                           (urc, scheme, target.uid))  # Unsure about what the target part should be, fix later.
        connection.commit()
    return urc


def send_email(target, urc):
    with smtplib.SMTP("smtp.gmail.com", 587).starttls() as server:
        with server.login(settings.cast.sender, settings.cast.password) as session:
            msg = MIMEText(TEXT_MESSAGE.format(**target._asdict(), link=URL + urc, ), 'html')
            msg['Subject'] = SUBJECT
            msg['From'] = settings.cast.sender
            msg['To'] = target.email
            session.sendmail(settings.cast.sender, target.email, msg.as_string())


def cast_net(targets, scheme):
    sent_count = 0
    for target in targets:
        urc = update_database(target, scheme)
        try:
            send_email(target, urc)
            sent_count += 1
        except:
            print("Failed to send to", target.email)
    print("Sent to ", sent_count, " email(s).")
