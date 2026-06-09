import imaplib
import smtplib
import email
import time
import os
import threading

from email.mime.text import MIMEText
from email.utils import parseaddr
from flask import Flask

# Environment variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

print("EMAIL =", EMAIL)
print("PASSWORD EXISTS =", PASSWORD is not None)

# Flask app (needed for Render Web Service)
app = Flask(__name__)

@app.route("/")
def home():
    return "Email Bot is Running!"


def send_reply(to_email):
    try:
        print("Sending reply to:", to_email)

        msg = MIMEText("""
Hello,

Thank you for contacting us.

We appreciate your interest in our services.

Our team specializes in:
• AI Automation
• Email Marketing
• Website Development
• Business Growth Solutions

We will get back to you soon.

Best regards,
AI Automation Team
""")

        msg["Subject"] = "Thank you for contacting us"
        msg["From"] = EMAIL
        msg["To"] = to_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()

        print("Reply sent successfully!")

    except Exception as e:
        print("SEND ERROR:", e)


def check_emails():
    try:
        print("Connecting to Gmail...")

        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

        print("Connected!")

        mail.login(EMAIL, PASSWORD)

        print("Logged in!")

        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")

        email_ids = messages[0].split()

        print("Unread emails:", len(email_ids))

        for e_id in email_ids:

            status, msg_data = mail.fetch(e_id, "(RFC822)")

            raw_email = msg_data[0][1]

            msg = email.message_from_bytes(raw_email)

            sender = parseaddr(msg["From"])[1]

            print("New email from:", sender)

            if sender.lower() != EMAIL.lower():
                send_reply(sender)

        mail.logout()

    except Exception as e:
        print("CHECK ERROR:", e)


def email_loop():
    while True:
        check_emails()
        time.sleep(120)


threading.Thread(target=email_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)