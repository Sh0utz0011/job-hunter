# Job Hunter 

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django 6.1](https://img.shields.io/badge/Django-6.1-0C4B33?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![httpx](https://img.shields.io/badge/httpx-async-0077B6?logo=python&logoColor=white)](https://www.python-httpx.org/)
[![pytest](https://img.shields.io/badge/pytest-passing-brightgreen?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Автоматический агрегатор вакансий для Python-разработчика.**  
> Парсит hh.ru API, хранит вакансии в БД, фильтрует по стеку технологий и присылает новые подходящие вакансии в Telegram.

## Зачем нужен проект

Ручной поиск работы отнимает часы каждый день: открыть hh.ru, отфильтровать по стеку (FastAPI/Django/Flask), отсеять нерелевантное, проверить, не видел ли эту вакансию раньше. Job Hunter делает это за меня — и заодно демонстрирует навыки backend-разработки на Django с TDD-подходом.

> Это второй пет-проект в моём портфолио. Первый — [Content Generator API](https://github.com/Sh0utz0011/content-generator) на FastAPI + Ollama (REST API для генерации контента локальной LLM Qwen 2.5).

## Возможности (MVP)

- **Парсинг hh.ru API** по настраиваемым поисковым запросам (Django management command)
- **Дашборд вакансий** со статистикой: средняя зарплатная вилка, % вакансий с указанной з/п, топ городов
- **Поиск по названию, компании и описанию** без перезагрузки страницы
- **Django Admin** для управления поисковыми запросами и просмотра вакансий
- **TDD**: модульные и интеграционные тесты с `httpx.MockTransport` (без реальных HTTP-запросов)
- **Graceful degradation**: при блокировке API (403) используется демо-источник для разработки/CI

## Стек технологий

| Слой | Технологии |
|---|---|
| **Backend** | Python 3.11+, Django 6.1 |
| **HTTP-клиент** | `httpx` (синхронный, с `MockTransport` в тестах) |
| **База данных** | SQLite (dev), PostgreSQL (prod, в разработке) |
| **Тестирование** | `pytest`, `django.test.TestCase`, `httpx.MockTransport` |
| **Контейнеризация** | Docker Compose (в разработке) |
| **CI/CD** | GitHub Actions (в разработке) |

> Стек сознательно пересекается с моим основным проектом на FastAPI: здесь я демонстрирую владение Django как вторым крупным фреймворком, оставаясь в знакомом pytest/TDD/Docker-окружении.

## Скриншоты

<!-- TODO: вставить скриншот дашборда после запуска seed_demo -->
> Дашборд с тёмной темой, статистикой, поиском и карточками вакансий.

## Быстрый старт

### Требования
- Python 3.11+
- pip

### Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Sh0utz0011/job-hunter.git
cd job-hunter

# 2. Создать и активировать виртуальное окружение
python -m venv .venv

# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Применить миграции
python manage.py migrate

# 5. Создать суперпользователя для Django Admin
python manage.py createsuperuser