import logging
_logger = logging.getLogger(__name__)
import datetime
import hashlib
import smtplib
from email.mime.text import MIMEText

import pymysql

from fishing_smile.settings import get_settings

settings = get_settings()

# Email subject.
SUBJECT = "Please change your Organization account password."
# Email body.
#TODO -- add Thai language version
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
# Link to target website.
URL = f"{settings.cast.url}/index.html?k="


def insert2db(addr, key_batch):
    # TODO -- change id/key-gen method
    id = hashlib.md5(addr.encode(), usedforsecurity=False)
    key = hashlib.md5(''.join([addr, str(key_batch)]).encode(), usedforsecurity=False)
    # TODO -- change sql query to match new db
    with pymysql.connect(settings().db.model_dump()) as connection:
        with connection.cursor() as cursor:
            sql = """
                  INSERT INTO fishlist (`ID`, `EMAIL`)
                  VALUES (%s, %s) \
                  """
            cursor.execute(id.hexdigest(), addr)
        connection.commit()
    return key.hexdigest()


def send_email(target, key):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(settings.cast.sender, settings.cast.password)
    text_body = TEXT_MESSAGE.format(
        **target._asdict(),
        link=URL + key,
    )
    msg = MIMEText(text_body, 'html')
    msg['Subject'] = SUBJECT
    msg['From'] = settings.cast.sender
    msg['To'] = target.email
    server.sendmail(SENDER, target.email, msg.as_string())
    server.quit()


def cast_net(targets):
    sent_count = 0
    key_batch = datetime.datetime.now()
    for target in targets:
        k = insert2db(target.email, key_batch)
        try:
            send_email(target, k)
            sent_count += 1
        except:
            print("Failed to send to", target.email)
    print("Sent to ", sent_count, " email(s).")
