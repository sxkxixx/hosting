<<<<<<< HEAD
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
=======
<h1>Проектный практикум ИРИТ-РТФ 2023</h1>
<h2>Разработка личного кабинета стажёра. Планировщик задач с диаграммой Ганта проектной работы</h2>
<br>
gant gant-chart
>>>>>>> acdc5c871dd2b6d017adfa09e8086501374023c9
