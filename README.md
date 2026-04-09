# VK PyBot

Бот для ВКонтакте на Python с игрой "Писюн" и системой рейтинга игроков.

## Описание

Простой бот для групповых чатов ВКонтакте с мини-игрой, где участники могут раз в день "крутить" случайное изменение своего показателя. Все данные хранятся в PostgreSQL.

## Возможности

- 🎲 Игра "/писюн" - ежедневная случайная прокрутка с изменением показателя
- 🏆 Команда "/топ" - рейтинг топ-10 игроков в чате
- 🏓 Команды "/пинг", "/понг", "/крым" для проверки работы бота
- 📊 Хранение данных в PostgreSQL с поддержкой нескольких чатов
- 🔄 Автоматическое создание таблиц при первом запуске

## Технологии

- Python 3.11
- [vkbottle](https://github.com/vkbottle/vkbottle) - фреймворк для VK Bot API
- SQLAlchemy (async) - ORM для работы с БД
- PostgreSQL 16 - база данных
- Docker & Docker Compose - контейнеризация
- Kubernetes - деплой в production

## Быстрый старт

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <repo-url>
cd vkpybot
```

2. Создайте `.env` файл на основе `.env.example`:
```bash
cp .env.example .env
```

3. Заполните переменные окружения в `.env`:
```env
BOT_TOKEN=your_vk_bot_token
POSTGRES_USER=vk_bot
POSTGRES_PASSWORD=your_password
POSTGRES_DB=vk_bot_db
```

4. Запустите через Docker Compose:
```bash
docker compose up -d
```

5. Проверьте логи:
```bash
docker compose logs -f bot
```

### Деплой в Kubernetes

1. Отредактируйте `k8s/deployment.yaml` и добавьте свои credentials в секцию Secret

2. Примените манифест:
```bash
kubectl apply -f k8s/deployment.yaml
```

3. Проверьте статус:
```bash
kubectl get pods -n vkbot
kubectl logs -n vkbot -l app=vkbot
```

Подробнее см. [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Структура проекта

```
vkpybot/
├── src/                    # Исходный код
│   ├── bot.py             # Точка входа
│   ├── config.py          # Конфигурация
│   ├── handlers/          # Обработчики команд
│   ├── db/                # Модели и подключение к БД
│   └── utils/             # Утилиты
├── k8s/                   # Kubernetes манифесты
├── scripts/               # Скрипты для деплоя и обслуживания
├── docs/                  # Документация
├── Dockerfile             # Docker образ
├── docker-compose.yml     # Локальная разработка
└── requirements.txt       # Python зависимости
```

## Команды бота

- `/писюн` - сыграть в игру (раз в день)
- `/топ` - показать топ-10 игроков чата
- `/пинг` - проверка работы бота
- `/понг` - шуточная команда
- `/крым` - патриотическая команда

## Разработка

### Требования

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16 (или через Docker)

### Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Запуск локально без Docker

```bash
# Убедитесь что PostgreSQL запущен
export POSTGRES_HOST=localhost
python -m src.bot
```

## Бэкапы

Автоматические ежедневные бэкапы настроены через Kubernetes CronJob.

Подробнее см. [docs/BACKUP.md](docs/BACKUP.md)

## Деплой

Для быстрого деплоя используйте скрипт:

```bash
./scripts/deploy.sh
```

Подробнее см. [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## Лицензия

MIT License - см. [LICENSE](LICENSE)

## Автор

ayne272
