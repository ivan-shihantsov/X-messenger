## Запуса сервера приложения в локальной сети (LAN) или на VPS

Допустим, у имеется несколько девайсов:<br>
* server IP: 192.168.100.60
* client 1 IP: 192.168.100.5
* client 2 IP: 192.168.100.6

Нужно создать виртуальную машину (ubuntu 24.04 LTS) с сетевым адаптером bridge<br>
После установки открыть сетевые настройки и установить профиль со static IP<br>
```
ip: 192.168.100.60/24
gw: 192.168.100.1
dns: 208.67.222.222
```

Установить nginx и настроить как reverse proxy server<br>
```
sudo apt update
sudo apt install nginx
```

Написать nginx config для приложения<br>
```
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/myproject
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/myproject
```

и поменять его содержимое этого config-а<br>
`sudo nano /etc/nginx/sites-available/myproject`
```
server {
	listen 80;
	server_name 192.168.100.60;

	location / {
		proxy_pass http://127.0.0.1:8001;
        	proxy_set_header Host $host;
        	proxy_set_header X-Real-IP $remote_addr;
        	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        	proxy_set_header X-Forwarded-Proto $scheme;
	}
}
```

проверить правильность нового config-а и перезагрузить nginx<br>
```
sudo nginx -t
sudo systemctl reload nginx
```

Подготовить сервер для работы с git<br>
```
sudo apt update
sudo apt install git
```

теперь репозиторий может быть клонирован по HTTPS (не по SSH, как при разработке), потому что серверу<br>
```
git clone https://github.com/ivanka6342/X-messenger.git ./myapp
cd myapp/
```

установить пакет python venv и использовать его<br>
```
sudo apt update
sudo apt install python3-venv

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

запустить приложение на flask (server.py) через gunicorn<br>
```
gunicorn --bind 0.0.0.0:8001 server:app
```

теперь можно делать запросы с клиентов (IP: 192.168.100.5 и 192.168.100.6) на сервер (IP: 192.168.100.60)<br>
