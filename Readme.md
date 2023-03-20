<h1>API</h1>
<h2>FASTApi</h2>

<h3>UserModel Auth</h3>
<ul>

    GET - /api/v1/auth (Авторизация)
    POST - /api/v1/signup (Регистрация)
</ul>
<h3>Video Service</h3>
<ul>
<h4>GET-requests</h4>

    GET - /api/v1/videos (Показ всех видео)
    GET - /api/v1/video/<int:id> (Показ конкретного видео)
    GET - /api/v1/video/<int:id>/likes (Лайки видео)
    GET - /api/v1/video/<int:id>/comments (Комментарии)

<h4>POST-requests</h4>

    POST - /api/v1/video/upload (Загрузка видео)
    POST - /api/v1/video/<int:id>/upload_comment (Публикация комментария)
    POST - /api/v1/video/<int:id>/like (Поставить лайк)

<h4>DELETE-request</h4>

    DELETE - api/v1/video/<int:id> (Удаление видео)
    DELETE - api/v1/video/<int:id>/comment/<int:id> (Удалить комментарий)
</ul>