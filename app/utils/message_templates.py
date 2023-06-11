from core.config import LINK


def on_register_template(email):
    return f"""<html>
    <head></head>
    <body>
        <h3>Здравствуйте, {email}!</h1>
        <h4>Сообщаю, что вы успешно зарегистрировались на <a href="{LINK}">VideoHosting</a></h2>
    </body>
    </html>"""


def on_delete_video_template(email):
    return f"""<html>
    <head></head>
    <body>
        <h3>Здравствуйте, {email}!</h1>
        <h4>Ваше видео было удалено админом с <a href="{LINK}">VideoHosting</a></h2>
    </body>
    </html>
    """


def on_delete_account_template(email):
    return f"""<html>
    <head></head>
    <body>
        <h3>Здравствуйте, {email}!</h1>
        <h4>Ваш аккаунт был удален с <a href="{LINK}">VideoHosting</a></h2>
    </body>
    </html>
    """
