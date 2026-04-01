# 🏓 Дальняя Зона — Форум по настольному теннису

Веб-форум для любителей настольного тенниса с интеграцией Telegram-бота для уведомлений из формы обратной связи.

**Демо:** https://farzone.onrender.com

---

## 📖 О проекте

Учебный проект, представляющий собой полноценный форум с возможностью:
- Публикации постов по категориям
- Комментирования постов
- Системой лайков в реальном времени (WebSocket)
- Личным профилем с информацией об оборудовании
- Формой обратной связи с уведомлениями в Telegram

---

## 🚀 Технологии

### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| **Django** | 5.1.7 | Основной фреймворк |
| **Django REST Framework** | 3.16.0 | REST API |
| **FastAPI** | 0.115.0 | Микросервис уведомлений |
| **Django Channels** | 4.2.2 | WebSocket поддержка |
| **Daphne** | 4.2.0 | ASGI сервер |

### База данных и кэш
| Технология | Назначение |
|------------|------------|
| **SQLite3** | Основное хранилище данных |
| **Redis** | Кэширование и Channels layer |

### Интеграции
| Сервис | Назначение |
|--------|------------|
| **Telegram Bot API** | Уведомления из формы обратной связи |
| **Yandex Maps API** | Карта на странице контактов |

### DevOps
| Технология | Назначение |
|------------|------------|
| **Docker** | Контейнеризация |
| **Render.com** | Хостинг |
| **GitHub Actions** | CI/CD |
| **Nginx** | Reverse proxy |

---

## 📁 Структура проекта

```
dalnyaya-zona/
├── farzone/                    # Django приложение
│   ├── farzone/               # Настройки проекта
│   ├── forum/                 # Приложение форума
│   │   ├── models.py          # Модели: Post, Category, Comment, PostLike, ContactMessage
│   │   ├── views.py           # Views для постов, комментариев, лайков
│   │   ├── forms.py           # Формы
│   │   ├── urls.py            # URL маршруты
│   │   ├── api/               # REST API endpoints
│   │   ├── consumers.py       # WebSocket consumers (лайки)
│   │   └── templates/         # HTML шаблоны
│   ├── users/                 # Приложение пользователей
│   │   ├── models.py          # Кастомная модель User
│   │   ├── views.py           # Аутентификация, профили
│   │   └── ...
│   ├── manage.py
│   └── requirements.txt
│
├── telegram-notifier/         # Микросервис уведомлений
│   ├── app/
│   │   ├── main.py            # FastAPI приложение
│   │   ├── tg.py              # Отправка в Telegram
│   │   └── config.py          # Конфигурация
│   └── requirements.txt
│
├── nginx.conf                 # Конфигурация Nginx
├── render.yaml                # Деплой на Render
├── Dockerfile.farzone         # Docker образ Django
├── Dockerfile.notifier        # Docker образ бота
└── .github/workflows/         # CI/CD пайплайны
```

---

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────────┐
│                        Пользователь                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Nginx (port 80)                          │
│  /static/ → staticfiles    /media/ → media                       │
│  /ws/     → WebSocket       /*       → Django                   │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────────┐
│   Django (Daphne:8000)  │     │   FastAPI (Uvicorn:8001)        │
│  - Форум                │     │  - Telegram Bot                 │
│  - REST API             │────▶│  - POST /notifications/         │
│  - WebSocket /ws/       │     │                                 │
└─────────────────────────┘     └─────────────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│   SQLite + Redis        │     │   Telegram Chat             │
└─────────────────────────┘     └─────────────────────────────┘
```

---

## ⚙️ Установка и запуск

### Требования
- Python 3.11+
- Docker (для продакшена)
- Redis (для кэширования и WebSocket)

### Локальная разработка

#### 1. Клонирование репозитория
```bash
git clone https://github.com/yourusername/dalnyaya-zona.git
cd dalnyaya-zona
```

#### 2. Настройка Django
```bash
cd farzone
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env
# Заполните переменные окружения
```

#### 3. Миграции и запуск
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

#### 4. Запуск Telegram-нотифайера
```bash
cd ../telegram-notifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Создайте .env с переменными:
# TELEGRAM_BOT_TOKEN=your_token
# TELEGRAM_CHAT_ID=your_chat_id
# API_KEY=secret-key

uvicorn app.main:app --reload --port 8001
```

### Переменные окружения

#### Django (farzone/)
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

REDIS_URL=redis://localhost:6379/0
YANDEX_MAPS_API_KEY=your-yandex-key

NOTIFIER_URL=http://localhost:8001
NOTIFIER_API_KEY=secret-key
```

#### Telegram Notifier
```env
TELEGRAM_BOT_TOKEN=bot_token_from_botfather
TELEGRAM_CHAT_ID=your_chat_id
API_KEY=secret-key
```

---

## 🐳 Docker запуск

### Сборка образов
```bash
docker build -f Dockerfile.farzone -t farzone .
docker build -f Dockerfile.notifier -t notifier .
```

### Запуск через docker-compose (локально)
```bash
docker-compose up -d
```

---

## 📡 API Endpoints

### Forum API
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/posts/` | Список всех постов |
| `POST` | `/api/posts/` | Создать пост |
| `GET` | `/api/categories/` | Список категорий |

### Users API
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/users/api/auth/` | Получить токен аутентификации |

### Notifier API
| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/notifications/` | Отправить уведомление в Telegram |

**Headers:**
```
X-API-Key: secret-key
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Имя",
  "email": "email@example.com",
  "message": "Текст сообщения"
}
```

---

## 🎯 Основные возможности

### Форум
- ✅ Категории постов
- ✅ Создание, редактирование, удаление постов
- ✅ Комментарии к постам
- ✅ Лайки в реальном времени (WebSocket)
- ✅ Пагинация постов

### Пользователи
- ✅ Регистрация / Вход / Выход
- ✅ Личный профиль с аватаром
- ✅ Информация об оборудовании (основание, накладки)
- ✅ Редактирование профиля

### Уведомления
- ✅ Форма обратной связи на главной
- ✅ Мгновенные уведомления в Telegram
- ✅ Асинхронная отправка через aiohttp

---

## 🔄 CI/CD

Проект использует GitHub Actions для автоматического деплоя на Render.

**Пайплайн при push в master:**
1. Сборка Docker образов
2. Деплой через Render API

**Требуемые GitHub Secrets:**
```
RENDER_API_KEY=your_api_key
RENDER_SERVICE_ID_FARZONE=service_id
RENDER_SERVICE_ID_NOTIFIER=service_id
```

---

## 📱 Telegram бот

Бот отправляет уведомления администратору при заполнении формы обратной связи на сайте.

---


## 👨‍💻 Автор

**Дмитрий Елтанский**
- Email: dmitriyeltanskiy48@yandex.ru
- Адрес: г. Москва, г. Зеленоград, ул. Юности, д.15

---

## 📄 Лицензия

Учебный проект. Все права защищены.

---

## Скриншоты:

<img width="1646" height="1012" alt="image" src="https://github.com/user-attachments/assets/9fbc4dd7-2220-4fff-a474-658b2da36158" />
<img width="1648" height="871" alt="image" src="https://github.com/user-attachments/assets/c9457ebf-09cc-42bb-834b-178f6eba7edf" />
<img width="1540" height="972" alt="image" src="https://github.com/user-attachments/assets/3b92a032-1c29-4b26-a8b6-572ad2714d2b" />
<img width="1543" height="986" alt="image" src="https://github.com/user-attachments/assets/6ec12166-6ab2-4613-a0c1-2b20e2d7945e" />


