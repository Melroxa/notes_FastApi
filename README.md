# Заметки - Приложение на FastAPI

Приложение для управления заметками с возможностью создания, редактирования, удаления и восстановления заметок. Пользователи могут работать с заметками, а администраторы могут управлять всеми заметками.

## Требования

Перед запуском убедитесь, что на вашем компьютере установлены:

- Docker
- Docker Compose

## Установка и запуск с помощью Docker

1. Клонируйте репозиторий:

   ```bash
   git clone (https://github.com/Melroxa/notes_FastApi.git)
   cd notes-app
   ```

2. Построение и запуск контейнеров с помощью Docker Compose:

   В каталоге проекта выполните команду:

   ```bash
   docker compose up --build
   ```

   Это создаст и запустит все необходимые контейнеры (включая контейнер для базы данных и для вашего приложения FastAPI).

3. Ожидайте завершения процесса сборки. Это займет некоторое время.

4. После успешного запуска, ваше приложение будет доступно по следующему адресу:

   ```
   http://localhost:8000
   ```

5. Для проверки, что приложение работает, откройте веб-браузер и перейдите по адресу `http://localhost:8000/docs`, чтобы увидеть автоматически сгенерированную документацию для вашего FastAPI приложения.

6. Если вы хотите остановить приложение, выполните команду:

   ```bash
   docker compose down
   ```

   Это остановит и удалит контейнеры, созданные при запуске.

## Структура проекта

- **app/**: Основной код приложения.
- **app/models.py**: Модели данных SQLAlchemy для базы данных.
- **app/database.py**: Настройки базы данных и подключения.
- **app/main.py**: Главный файл для запуска FastAPI приложения.
- **app/templates/**: HTML-шаблоны для отображения веб-страниц.
- **docker-compose.yml**: Конфигурация для запуска контейнеров.
- **Dockerfile**: Конфигурация для создания образа Docker.
- **requirements.txt**: Список зависимостей Python.
- **app/auth_utils.py**: Утилиты для работы с JWT-токенами.
- **app/utils.py**: Утилиты для работы с пользователями и паролями.
- **app/logger.py**: Логирование действий пользователей.
- **app/routers/auth.py**: Маршруты для аутентификации.
- **app/routers/notes.py**: Маршруты для работы с заметками.
- **app/schemas.py**: Схемы для сериализации данных.
