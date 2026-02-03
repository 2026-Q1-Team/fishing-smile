import hashlib
import numpy
import pymysql
import smtplib
import datetime
from email.mime.text import MIMEText
from pymysql.err import MySQLError

# Sender info (for SMTPlib)
SENDER = "siwapon.so11@gmail.com"
PASSWORD = "ajnr ulsc hxey tcnp"

# Email subject.
SUBJECT = "Please change your Organization account password."
# Email body. TODO add Thai language version
TEXT_MESSAGE = """Dear {name},
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
FORM_LINK = "http://hii-survey.secteam.in.th/index.html?k="


# =====================================================

def get_target(filename):
    tm = numpy.genfromtxt(filename, delimiter=',', dtype=str)
    return tm


def insert2db(addr):
    ID = hashlib.md5(addr.encode(), usedforsecurity=False)
    KEY = hashlib.md5(str(addr,key_batch).concat.encode(), usedforsecurity=False)
    try:
        con = pymysql.connect(user='tracker', password='fishtracker67', host='localhost', database='fishtrack')
        mycursor = con.cursor()
        sql = "INSERT INTO fishlist (ID, EMAIL) VALUES (%s, %s)"
        value = (ID.hexdigest(), addr)
        mycursor.execute(sql, value)
        con.commit()
        sql2 = "INSERT INTO fishcast (ID, KEY, BATCH) VALUES (%s, %s, %s)"
        value2 = (ID.hexdigest(), KEY.hexdigest(), key_batch)
        mycursor.execute(sql2, value2)
        con.close()
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" % (e.args[0], e.args[1]))
    return KEY.hexdigest()


def send_email(addr, name, key):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    text_body = TEXT_MESSAGE.format(name=name, link=FORM_LINK + key)
    msg = MIMEText(text_body, 'html')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = addr
    server.sendmail(SENDER, addr, msg.as_string())
    server.quit()


# ======================================================

if __name__ == "__main__":
    sent_count = 0
    key_batch = datetime.datetime.now()
    # Receiver matrix. Should be [['email','name_TH','name_EN']] when printed.
    MList = get_target(input("Enter filepath:"))
    for e in MList:
        key = insert2db(e[0])
        send_email(e[0], e[1], key)
        sent_count += 1
    print("Sent to ", sent_count, " email(s).")
