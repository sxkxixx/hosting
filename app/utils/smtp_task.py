import smtplib
from core.config import SMTP_EMAIL, SMTP_PASSWORD, SMTP_SERVER, LINK
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def template(email):
    return f"""<html>
    <head></head>
    <body>
        <h3>Hello, {email}!</h1>
        <h4>You've successfully signed up at <a href="{LINK}">VideoHosting</a></h2>
        <h4>I'm glad to see you at my study-project</h4>
    </body>
    </html>"""


def send_message(to_address: list | str = None):
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
        try:
            server.sendmail(from_addr=SMTP_EMAIL, to_addrs=address, msg=message.as_string())
        except:
            continue
    server.quit()
