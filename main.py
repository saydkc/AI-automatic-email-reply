import imaplib
import smtplib
import email
import time
import os
from email.message import EmailMessage

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def is_bot(sender):
    bot_keywords = ["noreply", "no-reply", "bot", "mailer", "notification", "google"]

    sender = sender.lower()

    for word in bot_keywords:
        if word in sender:
            return True

    return False


def send_advertisement(to_email):

    ad_message = """
Hello,

My name is Ali and I run an AI Automation service that helps businesses save time and reduce manual work.

Many companies spend a lot of time on repetitive tasks like replying to emails, handling customer questions, data entry, and marketing messages. With AI automation, these tasks can be done automatically.

Our AI solutions can help your business:
• Automatically reply to customer messages
• Send marketing emails to potential customers
• Organize and process business data
• Reduce employee workload
• Improve efficiency and productivity

If you are interested, I would be happy to show you how AI automation can help your business grow.

Please reply to this email if you would like to learn more.

Best regards,
ali
AI Automation Services

"""

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Save Time and Money with AI Automation"
    msg.set_content(ad_message)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()

    print("Advertisement sent to:", to_email)


def check_emails():

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)

    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()

    for e_id in email_ids:

        status, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        sender = msg["From"]

        print("New email from:", sender)

        if not is_bot(sender):
            send_advertisement(sender)
        else:
            print("Skipped bot email")

    mail.logout()


print("Email advertisement bot started")

while True:
    try:
        check_emails()
    except Exception as e:
        print("Error:", e)

    time.sleep(130)