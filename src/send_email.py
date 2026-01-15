import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import hashlib
import pymysql
from pymysql.err import MySQLError

# ==================== ตั้งค่าที่นี่ ====================
SENDER = "siwapon.so11@gmail.com"
PASSWORD = "ajnr ulsc hxey tcnp"

# รายชื่อผู้รับ (เพิ่มได้เรื่อยๆ)
RECEIVERS = [
    "siwapon.so11@gmail.com",
]

SUBJECT = "แบบประเมินความพึงพอใจด้านความสะอาดตู้กดน้ำในอาคาร ปี2569"

# Link แบบสอบถาม (Google Forms)
FORM_LINK = "http://203.185.101.156/index.html?k=2326c7e8efb1f97e6d47c16d22a7a6f4"

# Plain Text Message
TEXT_MESSAGE = """สวัสดีครับ/ค่ะ

ขอความร่วมมือทำแบบประเมินความพึงพอใจด้านความสะอาดของตู้กดน้ำภายในอาคาร
เพื่อนำข้อมูลไปปรับปรุงคุณภาพการดูแลรักษาความสะอาดให้ดียิ่งขึ้น

หัวข้อการประเมิน:
- ความสะอาดของตู้กดน้ำและบริเวณโดยรอบ
- คุณภาพน้ำดื่มจากตู้กดน้ำ
- ความถี่ในการทำความสะอาดและบำรุงรักษา
- ความสะดวกในการใช้งานและตำแหน่งที่ตั้ง

ใช้เวลาประมาณ 3-5 นาที

คลิกลิงก์เพื่อทำแบบประเมิน:
{form_link}

ขอบคุณสำหรับความร่วมมือครับ/ค่ะ
— สำนักงานพัฒนาวิทยาศาสตร์และเทคโนโลยีแห่งชาติ

ส่งเมื่อ: {timestamp}
"""
# =====================================================

def send_email():
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text_body = TEXT_MESSAGE.format(timestamp=timestamp, form_link=FORM_LINK)
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    
    for receiver in RECEIVERS:
        msg = MIMEText(text_body, 'plain', 'utf-8')
        msg['Subject'] = SUBJECT
        msg['From'] = SENDER
        msg['To'] = receiver
        
        server.sendmail(SENDER, receiver, msg.as_string())
        print(f"✅ ส่งถึง {receiver} เรียบร้อย!")
    
    server.quit()
    print(f"\n📧 ส่งอีเมลทั้งหมด {len(RECEIVERS)} คน เรียบร้อยแล้ว!")

def insertdb():
    pt = RECEIVERS[0]
    ct = hashlib.md5(pt.encode(), usedforsecurity=False)

    try:
        con = pymysql.connect(user='tracker', password='fishtracker67', host='localhost', database='fishtrack')

        mycursor = con.cursor()

        sql = "INSERT INTO fishlist (track_key, emailaddr) VALUES (%s, %s)"
        value = (ct.hexdigest(), RECEIVERS[0])
        mycursor.execute(sql, value)
        con.commit()
        con.close()

    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %(e.args[0], e.args[1]))

if __name__ == "__main__":
    print("=" * 40)
    print("🚀 Automatic Plain Text Email Sender")
    print("=" * 40)
    print(f"จาก: {SENDER}")
    print(f"ถึง: {', '.join(RECEIVERS)}")
    print(f"หัวข้อ: {SUBJECT}")
    print("=" * 40)
    
    send_email()
    insertdb()
