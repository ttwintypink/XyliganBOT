# Discord Random Role Bot (Linux)

Этот бот выдает **одну случайную роль** новому участнику при входе на сервер.

## Что внутри
- `bot.py` — основной файл бота
- `requirements.txt` — зависимости Python
- `.env.example` — пример переменных окружения
- `start.sh` — запуск бота
- `install_linux.sh` — быстрая установка на Linux-хост
- `random-role-bot.service` — шаблон для автозапуска через `systemd`

## Установка на Linux

### 1. Распакуй архив
```bash
unzip random_role_bot_linux.zip
cd random_role_bot_linux
```

### 2. Установи Python и venv
На Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### 3. Установи зависимости
```bash
./install_linux.sh
```

### 4. Создай `.env`
```bash
cp .env.example .env
nano .env
```

Вставь туда токен:
```env
DISCORD_TOKEN=PASTE_YOUR_BOT_TOKEN_HERE
# GUILD_ID=123456789012345678
```

## Запуск
```bash
source venv/bin/activate
./start.sh
```

## Автозапуск через systemd
Открой и отредактируй шаблон:
```bash
nano random-role-bot.service
```

Замени:
- `REPLACE_WITH_LINUX_USER` на пользователя Linux
- `REPLACE_WITH_PROJECT_PATH` на полный путь к папке проекта

Пример:
- пользователь: `root`
- путь: `/root/random_role_bot_linux`

Дальше:
```bash
sudo cp random-role-bot.service /etc/systemd/system/random-role-bot.service
sudo systemctl daemon-reload
sudo systemctl enable random-role-bot
sudo systemctl start random-role-bot
sudo systemctl status random-role-bot
```

## Важно в Discord
1. Включи **Server Members Intent** в Discord Developer Portal.
2. Выдай боту право **Manage Roles**.
3. Подними роль бота **выше всех ролей**, которые он должен выдавать.

## Логика
При входе пользователя бот:
1. берет список ролей из `ROLE_IDS`
2. проверяет, какие из них реально существуют на сервере
3. выбирает **одну случайную**
4. выдает ее новому участнику

## Изменение списка ролей
Открой `bot.py` и замени список `ROLE_IDS` на свой.
