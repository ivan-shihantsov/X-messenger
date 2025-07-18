## X-messenger

#### Цель проекта:
* разработать клиент-серверное приложение для обмена сообщениями между несколькими пользователями через Интернет


#### Задачи проекта:
1. создать минимально функциональное приложение для обмена сообщениями, что не подразумевает:
    * красоту (UI)
    * удобство (UX)
    * множество функций (отправка и просмотр файлов, изменение/удаление/пересылка сообщений)
    * качество кода (style-guide, паттерны проектирования)
    * правильность архитектуры (компоновка модулей, MVC)
    * безопасность обмена сообщениями (https, аутентификация юзера)
    * возможность подключить более 2 пользователей
2. понять клиент-серверную архитектуру. поэтому клиент и сервер будут:
    * 2-мя разными программами, а не подпроцессами одной программы
    * запускаться на разных устройствах с разными платформами
    * взаимодействовать удаленно, посредством http-запросов
    * написаны на разных языках
    * и даже храниться в разных репозиториях
3. научиться отличать понятия сервера
    * сервер (VDS) - удаленная машина, облачный компьютер с установленной ОС, с публично доступным IP-адресом, готовый запускать наш софт
    * сервер (приложение) - любое приложение, которое обрабатывает запросы пользователей (клиентов)
4. запуск сервера на удаленной машине для подключения пользователей через Интернет
    * до этого момента серверную часть приложения можно запускать в тестовом режиме локально - на одной машине с клиентской частью - для проверки работы. но другие Клиенты из Интернета в таком режиме подключиться не смогут
5. разработка на нескольких языках: Java + Python
    * важно показать, что крупные enterprise решения никогда не пишутся на одном языке
    * части, написанные на разных языках нормально стыкуются, запускают или вызывают друг друга, передают данные между собой - взаимодействуют через API (программные, сетевые и т.д.)
6. командная работа над кодом - освоить основы git
    * имеется в виду не совместная работа над одной задачей, а как раз раздельная работа над разными задачами - так, чтобы не создавать конфликтов в коде


#### Не является задачей:
1. создание красивого, удобного, полнофункционального мессенджера с визуальными изысками, UI/UX, оффлайн-функционалом
2. попытка конкурировать с телеграм или другими мессенджерами по функционалу (группы, каналы, охват аудитории)
3. создание коммерческого продукта, получение с этого прибыли и дальнейшая поддержка по достижении Цели
4. управление нагрузкой от множества пользователей и их данных
5. запуск на всевозможных платформах (смартфоны и ПК, Android и IOS, Windows/MacOS/Linux) с разными версиями ОС, хардверной базой, разрешениями экрана
    * вся разработка ведется в одинаковых условиях и строго в рамках проекта


#### Что нам понадобится:
1. git (не путать с GitHub) - для совместной работы с кодом и его загрузки уже как раз на GitHub
    * не забыть создать .gitignore для фильтрации мусора от IDE
2. чистый python (без IDE) - для разработки серверной части приложения на начальном этапе
    * и позже - для теста перед загрузкой на удаленный сервер - в близких к нему условиях, потому что там нет IDE, отладчиков, расширений и т.д.
    * requests (python модуль) / Curl / Postman - для имитации запросов клиента, пока он не будет реализован
3. Pycharm/VS Code (любая другая IDE) - для НОРМАЛЬНОЙ разработки серверной части приложения на Python + Flask
4. чистая java (jdk 24) - на начальном этапе, для разработки клиентской части приложения на компе - без смартфона
5. Android studio - для НОРМАЛЬНОЙ разработки клиентского приложения для смартфона на Java
    * android-смартфон в режиме разработчика
6. VDS - аренда удаленного сервера для загрузки на него приложения и запуска
    * VirtualBox - для теста архитектуры приложения в локальной сети (дома)


#### Этапы разработки:
1. [Локальный](docs/pics/scheme-1.png): клиент и сервер запускаются на десктопе каждого разработчика. Общение по сети невозможно, важны функциональность и взаимодействие клиента и сервера. Здесь и далее код синхронизируется через GitHub <br>
![do not forget to update pic when update the scheme file](docs/pics/scheme-1.png "local dev scheme") <br>

2. [Полномасштабный](docs/pics/scheme-2.png): серверная часть запущена на VDS, клиент запускается на смартфонах разработчиков, возможно общение через сервер в интернете <br>
![do not forget to update pic when update the scheme file](docs/pics/scheme-2.png "full prod scheme") <br>


#### Порядок подготовки python venv для сервера
* python -m venv venv                   `# создание чистого локального python venv`
* .\venv\Scripts\activate               `# вход в него`
* python -m pip install --upgrade pip   `# обновление venv`
* pip install -r requirements.txt       `# установка необходимых для работы модулей внутри venv`
`NOTE: при создании requirements.txt в него записывается не вся выдача pip freeze, а только первично необходимые модули, например flask - его зависимости все равно установятся с ним`


#### Запуск сервера - локально
Предполагается, что python venv для сервера к этому моменту настроена<br>
* cd X-messenger            `# зайти в папку X-messenger`
* .\venv\Scripts\activate   `# войти в python virtual env`
* python server.py          `# запуск сервера`

обращаться к нему можно будет по внутрисистемному IP (loopback): localhost или 127.0.0.1 <br>
http://localhost:8001 <br>
например, при разработке серверной стороны эмулировать запросы клиента из Postman или curl <br>
при разработке клиента, запросы на localhost не идут из эмулятора в Android Studio - там уже нужен сервер с нормальным IP (хотя бы домашней сети - 192.168.0.0/24) <br>


#### Запуск сервера - на удаленном серваке
Предполагается, что python venv для сервера к этому моменту настроена<br>
Для запуска серверного приложения на удаленном сервере нужно следовать [инструкции](./install-guide.md) <br>
если кратко, то так: <br>
```
* cd X-messenger            				`# зайти в папку X-messenger`
* .\venv\Scripts\activate   				`# войти в python virtual env`
* gunicorn --bind 0.0.0.0:8001 server:app	`# запуск сервера`
```

gunicorn запускается только в Linux - нужна виртуальная машина<br>


#### Доступ к серверу (HTTP request)
Клиентским приложением может быть что угодно.<br>
Например, запросы к серверу можно делать через cURL:
```
# .\curl.exe -X 'POST' http://localhost:8001/sendMsg -H 'Content-Type: application/json' -d '{ \"username\":\"terminator\", \"toUser\":\"user1\", \"msg\":\"hello man\"}'
```
Также можно через python:
```
import requests

url = 'http://localhost:8001/sendMsg'
data = {"username":"terminator", "toUser":"user1", "msg":"hello man"}
response = requests.post(url, data=data)
```
Если это GET-запрос (c POST так не получится) и используется XML/SOAP, а не схема с JSON (хедер -H 'Content-Type: application/xml' вместо -H 'Content-Type: application/json'), тогда для проверки можно вставить строку с параметрами прямо в адресную строку браузера:
```
http://localhost:8001/sendMsg?username=terminator&toUser=user1&msg=hello
```


#### Технологии
* git (+ GitHub)
* Windows PowerShell
* python3 + Flask
* python venv (virtual environment)
* requests (python модуль) / Curl / Postman
* java + Android
* SQL (SQLite3 и MySQL)
* Nginx (web-server) + Gunicorn (WSGI-server)
* VirtualBox


#### Выводы
* гит важен для отслеживания версий кода, решения конфликтов в коде, сохранения кода
    * основы гит
* venv
    * .gitignore - его надо настраивать под проект


#### Возможные доработки
* когда юзер вызывает /add2chat, он не сразу добавляется в чат, а высылает запрос и ждет, пока его одобрит админ. тут же вариант развития публичных групп, каналов, где запросы/одобрения не нужны
* когда админ добавляет кого-то в чат, это не срабатывает мгновенно, а юзеру высылается запрос и ожидается его одобрение
* несколько админов в чате
* пересылка сообщений
* удаление сообщений - нужно оставлять их в пересланных или нет?
* удаление сообщений для себя/для всех
* когда юзер добаляется/удаляется из чата - видно техническое сообщение об этом (добавление типов сообщений)
* мультиязычный интерфейс - можно добавить модуль переводов, типа i18n
* удаление юзера - остаются ли его данные? нужно для видимости в чатах `<deleted account>` и в пересланных сообщениях
* частичная отправка сообщений оффлайн - с полной выгрузкой в сеть при включении инета + синхронизация с загруженными (написанными другими юзерами за время, пока был оффлайн)
* возможность переименовать юзера локально, а не только видеть его username
* возможность отправлять файлы
* возможность открывать медиаконтент прямо в прилаге - фото, видео
* запись контента прямо из прилаги (голосовые сообщения, видео)
* даты рождения и напоминалки о них
* многопоточная обработка клиентов сервером
* бэкапы данных
* галочки статуса сообщений: "доставлено", "прочитано"
* вместо точного поиска юзеров и чатов сделать поиск частичный (подстрока в строке) или поиск с ошибками (внешний модуль, вроде FuzzyWuzzy)
* сделать прилаге иконку в анроид, чтоб на рабочем столе отображалась не дефолтная
* добавить фичу 'Clean History' - удалить сообщения в чате
* возможность 'Delete Chat' - удалить чат целиком
* добавить не просто чаты, а контакты/друзья. с другом может не быть чата, а чат может быть не с другом
* возможность переименовать свой контакт по своему желанию
* возможность админа давать юзерам админку в чате
