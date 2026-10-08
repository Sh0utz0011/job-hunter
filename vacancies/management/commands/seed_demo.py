from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from vacancies.models import Vacancy

DEMO_VACANCIES = [
    {"external_id": "demo-01", "title": "Junior Python Developer", "company": "ЦЕНТР ИТ",
     "area_name": "Томск", "salary_from": 60000, "salary_to": 90000, "currency": "RUB",
     "snippet": "FastAPI, PostgreSQL, Docker: REST API для внутренних сервисов компании."},
    {"external_id": "demo-02", "title": "Python Backend Developer (Junior)", "company": "СберТех",
     "area_name": "Москва", "salary_from": 100000, "salary_to": 140000, "currency": "RUB",
     "snippet": "Микросервисы на FastAPI, интеграционные тесты, CI/CD."},
    {"external_id": "demo-03", "title": "Junior Django Developer", "company": "Электронный город",
     "area_name": "Новосибирск", "salary_from": 70000, "salary_to": 100000, "currency": "RUB",
     "snippet": "Развитие CRM на Django: ORM, admin-панель, формы."},
    {"external_id": "demo-04", "title": "Python-разработчик (парсинг)", "company": "ParseTech",
     "area_name": "Удалённо", "salary_from": 50000, "salary_to": 80000, "currency": "RUB",
     "snippet": "Парсинг данных: aiohttp, BeautifulSoup, Selenium, очереди задач."},
    {"external_id": "demo-05", "title": "Junior FastAPI Developer", "company": "Т-Банк",
     "area_name": "Удалённо", "salary_from": 90000, "salary_to": 130000, "currency": "RUB",
     "snippet": "REST API платёжных сервисов, Pydantic, pytest, TDD."},
    {"external_id": "demo-06", "title": "Backend Developer (Flask)", "company": "Skyeng",
     "area_name": "Москва", "salary_from": 80000, "salary_to": 120000, "currency": "RUB",
     "snippet": "Микросервисы на Flask, SQLAlchemy, PostgreSQL."},
    {"external_id": "demo-07", "title": "Junior Python Developer (Telegram-боты)", "company": "Пиксель",
     "area_name": "Томск", "salary_from": 45000, "salary_to": 70000, "currency": "RUB",
     "snippet": "Telegram-боты на aiogram, интеграции с CRM, вебхуки."},
    {"external_id": "demo-08", "title": "Python Developer (data pipeline)", "company": "Ozon Tech",
     "area_name": "Санкт-Петербург", "salary_from": 110000, "salary_to": 150000, "currency": "RUB",
     "snippet": "ETL-пайплайны, PostgreSQL, Docker; Airflow — обучим."},
    {"external_id": "demo-09", "title": "Стажёр Python-разработчик", "company": "Яндекс",
     "area_name": "Удалённо", "salary_from": 40000, "salary_to": 60000, "currency": "RUB",
     "snippet": "Backend-сервисы, код-ревью, тесты; наставничество."},
    {"external_id": "demo-10", "title": "Junior Backend Developer (LLM)", "company": "AI Start",
     "area_name": "Удалённо", "salary_from": 80000, "salary_to": 110000, "currency": "RUB",
     "snippet": "Интеграция локальных LLM (Ollama, Qwen) в backend-сервисы."},
]


class Command(BaseCommand):
    help = "Наполняет базу демо-вакансиями (разработка, скриншоты, CI)"

    def handle(self, *args, **options):
        now = timezone.now()
        created = 0
        for i, data in enumerate(DEMO_VACANCIES):
            _, is_created = Vacancy.objects.get_or_create(
                external_id=data["external_id"],
                defaults={
                    **data,
                    "url": f"https://hh.ru/vacancy/{90000000 + i}",
                    "published_at": now - timedelta(hours=i * 5 + 1),
                },
            )
            created += is_created
        self.stdout.write(self.style.SUCCESS(f"Демо-вакансий создано: {created}"))