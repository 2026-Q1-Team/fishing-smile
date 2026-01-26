import smtplib
from email.mime.text import MIMEText
import hashlib
import pymysql
from pymysql.err import MySQLError

# Sender info (for SMTPlib)
SENDER = "siwapon.so11@gmail.com"
PASSWORD = "ajnr ulsc hxey tcnp"

# Receiver matrix. Use ['email','name']. TODO add Thai name column
MList = [
    ['siwapon.so11@gmail.com', 'Siwapon'],
]
# Email subject.
SUBJECT = "Please change your Organization account password."

# Link to target website.
FORM_LINK = "http://hii-survey.secteam.in.th/index.html?k="

# Email body. TODO add Thai language version
TEXT_MESSAGE = """Dear {name},
According to our new security policy, all Organization staff must change their password every 6 months.
Follow these steps below to change your Organization account password.
    Step 1. Go to {link}.
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


# =====================================================

def send_email(addr,name,key):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    text_body = TEXT_MESSAGE.format(name=name, link=FORM_LINK+key)
    msg = MIMEText(text_body, 'plain', 'utf-8')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = addr
    server.sendmail(SENDER, addr, msg.as_string())
    server.quit()


def insert2db(addr):
    ct = hashlib.md5(addr.encode(), usedforsecurity=False)
    try:
        con = pymysql.connect(user='tracker', password='fishtracker67', host='localhost', database='fishtrack')
        mycursor = con.cursor()
        sql = "INSERT INTO fishlist (track_key, emailaddr) VALUES (%s, %s)"
        value = (ct.hexdigest(), addr)
        mycursor.execute(sql, value)
        con.commit()
        con.close()
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))
    return ct.hexdigest()

if __name__ == "__main__":
    sent_count = 0
    for e in MList:
        key = insert2db(e[0])
        send_email(e[0],e[1],key)
        sent_count += 1
        print("Sent to "+sent_count+" email(s).")
