## Cutaway site
### Технологии
<p>
<img src="https://www.django-rest-framework.org/img/logo.png" title="DRF" height="50"/>
<img src="https://starsl.cn/static/img/article/27.png" title="Django" height="50"/>
<img src="https://static.tildacdn.com/tild3333-3732-4033-a562-333462646536/Telegram_Final.png" title="TG API" height="50"/>
<img src="https://docs.aiohttp.org/en/stable/_static/aiohttp-plain.svg" title="Aiohttp" height="50"/>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1200px-Postgresql_elephant.svg.png" title="PostgreSQL" height="50"/>
<img src="https://assets.zabbix.com/img/brands/rabbitmq.svg" title="RabbitMQ" height="50"/>
<img src="https://files.virgool.io/upload/users/30711/posts/mivbx6r9geed/nwqgenmrbrfc.jpeg" title="Asyncio" height="50"/>
<img src="https://logos-download.com/wp-content/uploads/2021/01/Swagger_Logo-1536x1536.png" title="Swagger" height="50"/>
<img src="https://w7.pngwing.com/pngs/34/543/png-transparent-docker-plain-wordmark-logo-icon-thumbnail.png" title="Docker" height="50"/>
<img src="https://res.cloudinary.com/postman/image/upload/t_team_logo/v1629869194/team/2893aede23f01bfcbd2319326bc96a6ed0524eba759745ed6d73405a3a8b67a8" title="Postman" height="50"/>
<img src="https://marshmallow.readthedocs.io/en/stable/_static/marshmallow-logo.png" title="Marshmallow" height="100"/>
</p>

**Собрать и запустить контейнер**        
```docker-compose up -d --build```

✔ Реализовано на Django + DRF + PostgreSQL.<br>
✔ Процесс авторизации и регистрации, поддержка личного кабинета с возможностью изменения данных и удаления
        профиля.<br>
✔ Сервис блога: предполагает возможность написания своих постов и управления ими, подписки на других авторов,
        просмотр блогов конкретных авторов или тех, что добавлены в избранное.<br>
Ссылки для новых постов создаются автоматически.<br>
✔ Подключен API для выбора фильмов (рандомно по заданным параметрам), использована база кинопоиска.<br>
✔ Настроено кэширование, подсчет уникальных посещений страниц через мидлвар, проверка сессий.<br>
✔ Оптимизированы запросы к БД.<br>
✔ Добавлены капчи, а то вдруг будет восстание машин.<br>
✔ Фронт реализован на HTML + CSS + JS.<br>
✔ Интегрирована платежная система WebMoney.<br>
✔ Автоматическая сборка контейнера и пуш на докерхаб через Github Actions.<br>
✔ Бот - реализован на Aiohttp + Telegram API.<br>
✔ Для повышения отказоустойчивости всего приложения использован брокер сообщений - RabbitMQ.