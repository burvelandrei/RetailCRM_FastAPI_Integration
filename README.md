# RetailCRM_FastAPI_Integration 📦

API для взаимодействия с **RetailCRM** — работа с клиентами и заказами через **FastAPI**.
## 🔧 Стек технологий

- **FastAPI** – веб-фреймворк для создания API.
- **Pydantic** – валидация данных.
- **Docker, Docker Compose** – контейнеризация.
- **HTTpx** – для работы с API RetailCRM.

## 📋 Требования
- Установленный [Docker](https://www.docker.com/get-started).
- Установленный [Docker Compose](https://docs.docker.com/compose/install/).

## 🚀 Шаги по разворачиванию с Docker

1. **Создание директории приложения и переход в неё**:

   ```bash
   mkdir RetailCRM_FastAPI_Integration && cd RetailCRM_FastAPI_Integration
   ```

2. **Создание локальных папок для volume**:

   ```bash
   mkdir logs
   ```

3. **Копирование `docker-compose.yml` из репозитория**:

   ```bash
   wget https://raw.githubusercontent.com/burvelandrei/RetailCRM_FastAPI_Integration/main/docker-compose.yml
   ```

4. **Получение Subdomain и ключа API**:

   - Перейдите в [RetailCRM](https://www.retailcrm.ru/) и зарегистрируйтесь.
   - Создайте API ключ для интеграции.
      - Перейдите в меню Настройки → Интеграция → Добавить
      - Сгенерируйте API ключ

5. **Создание `.env` файла**:

    Создайте файл `.env` и добавьте следующие переменные:
    
    ```env
    RETAILCRM_SUBDOMAIN=your-subdomain
    RETAILCRM_API_KEY=your-api-key
    ```


6. **Запуск проекта через Docker Compose**:

   ```bash
   docker-compose up -d
   ```
7. **Проверка работоспособности**:
   - Откройте браузер и перейдите по адресу `http://your-host:8001/docs` для доступа к документации API.
   - Убедитесь, что контейнеры запущены: `docker-compose ps`.
---

📌 **Автор:** [burvelandrei](https://github.com/burvelandrei)
