import celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER
import logging

celery_app = celery.Celery('tasks', broker='redis://localhost:6379')
logging.basicConfig(filename='logs.log', level=logging.INFO)


def template(email):
    return f"""<html>
    <head></head>
    <body>
        <h3>Hello, {email}!</h1>
        <h4>You've successfully signed up at <a href="https://t.me/sxkxixx">VideoHosting</a></h2>
    </body>
    </html>"""


@celery_app.task()
def send_message(to_address: list | str = None):
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        if isinstance(to_address, str):
            to_address = [to_address]
        for address in to_address:
            message = MIMEMultipart()
            message['From'] = SMTP_EMAIL
            message['To'] = address
            message['Subject'] = 'Регистрация на видеохостинге'
            message.attach(MIMEText(template(address), 'html'))
            server.sendmail(from_addr=SMTP_EMAIL, to_addrs=address, msg=message.as_string())
        server.quit()
    except Exception:
        logging.warning(f'Send Email: Exception while sending to {to_address}')
