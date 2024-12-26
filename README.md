# Заметки - Приложение на FastAPI

Приложение для управления заметками с возможностью создания, редактирования, удаления и восстановления заметок. Пользователи могут работать с заметками, а администраторы могут управлять всеми заметками.

## Требования

Перед запуском убедитесь, что на вашем компьютере установлены:

- Docker
- Docker Compose

## Установка и запуск с помощью Docker

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/your-repo/notes-app.git
   cd notes-app
   ```

2. Построение и запуск контейнеров с помощью Docker Compose:

   В каталоге проекта выполните команду:

   ```bash
   docker-compose up --build
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
   docker-compose down
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

## Как это работает

### auth_utils.py

Этот файл содержит функции для создания и декодирования JWT токенов, которые используются для аутентификации пользователей.

- **create_access_token**: Создает JWT токен с заданными данными и временем жизни.
- **decode_access_token**: Декодирует токен и проверяет его валидность.

### utils.py

Файл содержит функции для работы с пользователями:

- **verify_token**: Верификация JWT токена.
- **get_current_user**: Извлекает текущего пользователя из токена.
- **hash_password**: Хэширует пароль пользователя с использованием библиотеки `bcrypt`.
- **verify_password**: Проверяет, совпадает ли введенный пароль с хэшированным паролем.
- **register_user**: Логика регистрации пользователя.

### logger.py

Этот файл отвечает за логирование действий пользователей в приложении:

- **log_action**: Логирует действия, записывая их в файл `actions.log`.

### routers/auth.py

Этот файл содержит маршруты для аутентификации пользователя:

- Регистрация пользователя.
- Вход в систему и получение JWT токена.
- Верификация токена и получение данных пользователя.

### routers/notes.py

Файл с маршрутами для работы с заметками:

- Создание, редактирование, удаление и восстановление заметок.
- Получение списка всех заметок и заметок по фильтрам.

### schemas.py

Этот файл содержит Pydantic схемы для сериализации данных:

- **UserCreate**: Схема для создания пользователя.
- **UserResponse**: Схема для отображения пользователя.
- **NoteCreate**: Схема для создания заметки.
- **NoteResponse**: Схема для отображения заметки.
