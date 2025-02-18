import smtplib
import ssl
from email.message import EmailMessage
from os import getenv

from aquasensor_backend.templates import env as jinja_env

# Email credentials
SMTP_SERVER = getenv("SMTP_SERVER")
SMTP_PORT = int(getenv("SMTP_PORT", 465))  # Use 587 for TLS, 465 for SSL
EMAIL_SENDER = getenv("EMAIL_SENDER")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

assert SMTP_SERVER is not None, "SMTP_SERVER environment variable is not set"
assert SMTP_PORT > 0 and SMTP_PORT < 65536, "SMTP_PORT environment variable is invalid"
assert EMAIL_SENDER is not None, "EMAIL_SENDER environment variable is not set"
assert EMAIL_PASSWORD is not None, "EMAIL_PASSWORD environment variable is not set"

def send_email(to: str, subject: str, template: str, template_data: dict):

    template = jinja_env.get_template("email/email.html")
    body = template.render(**template_data)

    try:
        # Create an email message object
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = to

        # Establish a secure SSL connection and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

