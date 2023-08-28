<h1>Видеохостинг</h1>
<h2>Зачетный проект для курса от АО "Точка"</h2>


<h3>Стек разработки:</h3>
<ul>
    <li>FastAPI - Серверная часть</li>
    <li>React.js - Клиентская часть</li>
    <li>PostgreSQL - База данных</li>
    <li>Docker, Docker Compose - Контейнеризация</li>
</ul>

<h3>Инструкция по запуску:</h3>
<ul>
    <li><b>git clone</b> <a>https://github.com/sxkxixx/hosting.git</a></li>
    <li><b>cd</b> hosting/</li>
    <li><b>touch</b> .env && Заполните .env необхоимыми параметрами*</li>
    <li><b>cd</b> front/ && <b>touch</b> .env, Заполните необходимые параметры**</li>
    <li>В файле docker-compose.yml укажите свои данные для контейнера 'db'***</li>
    <li>Из директории hosting/ выполните команду docker-compose up --build</li>
</ul>

<h3>Приложение:</h3>
<h4>* - Параметры для .env в директории hosting/</h4>
<ul>
    <li>SECRET_KEY</li>
    <li>ALGORITHM</li>
    <li>AWS_ACCESS_KEY_ID</li>
    <li>AWS_SECRET_ACCESS_KEY</li>
    <li>REGION_NAME</li>
    <li>BUCKET_NAME</li>
    <li>AVATARS_DIR</li>
    <li>VIDEOS_DIR</li>
    <li>PREVIEWS_DIR</li>
    <li>SAME_SITE</li>
    <li>POSTGRES_USER</li>
    <li>POSTGRES_PASSWORD</li>
    <li>POSTGRES_DB</li>
    <li>POSTGRES_HOST</li>
    <li>POSTGRES_PORT</li>
    <li>LINK</li>
    <li>CORS_HOST</li>
    <li>SMTP_EMAIL</li>
    <li>SMTP_PASSWORD</li>
    <li>SMTP_SERVER</li>
</ul>
<h4>** - Параметры для .env в директории hosting/front/</h4>
<ul><li>REACT_APP_API_URL</li></ul>
<h4>*** - Параметры для контейнера 'db' в файле docker-compose.yml</h4>
<ul>
    <li>POSTGRES_USER</li>
    <li>POSTGRES_PASSWORD</li>
    <li>POSTGRES_DB</li>
</ul>

