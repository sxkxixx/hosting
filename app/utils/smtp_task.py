import smtplib
from core.config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_message(subject, template, to_address: list | str = None):
    server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    if isinstance(to_address, str):
        to_address = [to_address]
    for address in to_address:
        message = MIMEMultipart()
        message['From'] = SMTP_EMAIL
        message['To'] = address
        message['Subject'] = subject
        message.attach(MIMEText(template(address), 'html'))
        try:
            server.sendmail(from_addr=SMTP_EMAIL, to_addrs=address, msg=message.as_string())
        except:
            continue
    server.quit()
