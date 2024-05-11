import os
from dotenv import load_dotenv
import smtplib, ssl

from Utlis.config_handler import ConfDataType, get_config_data

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()   # Load .env file


# Default addresses
__SENDER_EMAIL = os.getenv("SENDER_EMAIL", default="Value SENDER_EMAIL does not exist")
__SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', default="Value SENDER_PASSWORD does not exist")
__RECEIVER_EMAIL = get_config_data(ConfDataType.ADMINDATA)['admin-mail-address']



def send_alert_mail(body="No specific data",
                    subject="ALERT: The Google Cloud Agent detected problem"):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = __SENDER_EMAIL
    message["To"] = __RECEIVER_EMAIL
    message["Bcc"] = __RECEIVER_EMAIL

    message["Subject"] = subject
    message.attach(MIMEText(body, 'plain'))

    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(__SENDER_EMAIL, __SENDER_PASSWORD)             # Login to server
        server.sendmail(__SENDER_EMAIL, __RECEIVER_EMAIL, text)     # Send mail
