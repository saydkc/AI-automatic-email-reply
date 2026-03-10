
import imaplib
import smtplib
import email
import time
import os
from email.mime.text import MIMEText
from email.utils import parseaddr
from flask import Flask

# Gmail login
EMAIL = "yourgmail@gmail.com"
PASSWORD = "your_app_password"

app = Flask(__name__)

@app.route("/")
def home():
    return "Email bot running"


def check_emails():
    try:
        print("Checking inbox...")

        # Connect to Gmail IMAP
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, '(UNSEEN)')
        email_ids = messages[0].split()

        print("Unread emails:", len(email_ids))

        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]

            msg = email.message_from_bytes(raw_email)

            sender = parseaddr(msg["From"])[1]
            subject = msg["Subject"]

            print("New email from:", sender)
            print("Subject:", subject)

            send_reply(sender)

        mail.logout()

    except Exception as e:
        print("Error:", e)


def send_reply(to_email):
    try:
        print("Sending reply to:", to_email)

        msg = MIMEText(
            """Hello,
    
            Thank you for contacting us.
    
            We appreciate your interest in our services. Our team specializes in AI automation, email marketing tools, and digital solutions that help businesses grow faster.
    
            What we offer:
            • AI automation tools
            • Email marketing systems
            • Website and software development
            • Business growth strategies
    
            If you would like to learn more, feel free to reply to this email or visit our website.
    
            Best regards,
            AI Automation Team
            """
        )


        msg["Subject"] = "Save Time and Money with AI Automation"
        msg["From"] = EMAIL
        msg["To"] = to_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        print("Reply sent successfully!")

    except Exception as e:
        print("Send error:", e)


def email_loop():
    while True:
        check_emails()
        time.sleep(120)  # check every 2 minutes


import threading
threading.Thread(target=email_loop).start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)