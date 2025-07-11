# User Profile Microservice

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL/PostGIS](https://img.shields.io/badge/PostGIS-16--3.5-blue?logo=postgresql)](https://postgis.net/)
[![Redis](https://img.shields.io/badge/Redis-5.2.1-red?logo=redis)](https://redis.io/)
[![Docker Compose](https://img.shields.io/badge/Docker--Compose-3.9-blue?logo=docker)](https://docs.docker.com/compose/)
[![Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python)](https://www.python.org/)

---

## Описание

Асинхронный микросервис для управления профилями
пользователей с поддержкой геолокационного поиска, кэширования и JWT-аутентификации.
Сервис построен на FastAPI, использует PostgreSQL с расширением PostGIS для хранения
геоданных и Redis для кэширования.

---

## 🚀 Основные возможности

- Регистрация и обновление профиля пользователя (с валидацией возраста 18+)
- Поиск профилей по радиусу и возрасту (геолокация через PostGIS)
- Кэширование результатов поиска в Redis (ускорение повторных запросов)
- JWT-аутентификация (доступ только с валидным токеном)
- Асинхронная работа с БД и кэшем
- Докеризация и миграции через Alembic

## 🛠️ Технологический стек

- **Python 3.12** — основной язык разработки
- **FastAPI** — современный асинхронный web-фреймворк
- **SQLAlchemy** — ORM для работы с базой данных (async)
- **Alembic** — миграции схемы БД
- **PostgreSQL + PostGIS** — реляционная база данных с поддержкой геоданных
- **Redis** — кэширование и хранение сессий (асинхронный доступ)
- **Docker, docker-compose** — контейнеризация и оркестрация сервисов
- **Poetry** — управление зависимостями и пакетами
- **Pydantic** — валидация и сериализация данных
- **ruff** — быстрый и современный линтер для Python

---

### Слои приложения

- **Контроллеры**: обработка HTTP-запросов, валидация, возврат ошибок
- **Сервисы**: бизнес-логика, кэширование, агрегация данных
- **Репозитории**: работа с БД через SQLAlchemy
- **Кэш**: асинхронное взаимодействие с Redis
- **Модели и схемы**: структура данных, Pydantic и SQLAlchemy
- **Исключения**: централизованная обработка ошибок

---

## Быстрый старт

### Развертывание с помощью Docker

1. Создайте папку с проектом и склонируйте репозиторий:

```bash
mkdir user_profile_service
cd user_profile_service
git clone https://github.com/aquaracer/Fastapi-User-Profile-Microservice.git
```

2. Настройте переменные окружения в файле .env

3. Соберите и запустите контейнеры:

```bash
docker-compose up --build
```

4. Примените миграции базы данных:

```bash
docker exec -it user_profile_service bash
poetry run alembic upgrade head
```

Приложение будет доступно по следующим адресам:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

