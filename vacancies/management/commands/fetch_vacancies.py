from django.core.management.base import BaseCommand

from vacancies.models import SearchQuery, Vacancy
from vacancies.services.hh_client import fetch_vacancies


class Command(BaseCommand):
    help = "Загружает вакансии с hh.ru по активным поисковым запросам"

    def handle(self, *args, **options):
        total_new = 0
        for sq in SearchQuery.objects.filter(is_active=True):
            items = fetch_vacancies(sq.text, sq.area)
            new = 0
            for data in items:
                _, created = Vacancy.objects.get_or_create(
                    external_id=data["external_id"], defaults=data
                )
                new += created
            total_new += new
            self.stdout.write(f"[{sq}] загружено: {len(items)}, новых: {new}")
        self.stdout.write(self.style.SUCCESS(f"Готово. Всего новых: {total_new}"))