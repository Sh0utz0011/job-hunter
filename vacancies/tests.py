import httpx
from django.test import TestCase
from django.urls import reverse

from .models import Vacancy
from .services.hh_client import fetch_vacancies

PAYLOAD = {"items": [{
    "id": "42",
    "name": "Junior Python Developer",
    "employer": {"name": "Center IT"},
    "alternate_url": "https://hh.ru/vacancy/42",
    "salary": {"from": 80000, "to": 120000, "currency": "RUB"},
    "area": {"name": "Томск"},
    "published_at": "2026-10-06T10:00:00+0300",
    "snippet": {"requirement": "<b>Python</b>, Django", "responsibility": ""},
}]}


class HHClientTests(TestCase):
    def test_parses_items(self):
        client = httpx.Client(transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json=PAYLOAD)
        ))
        result = fetch_vacancies("python", client=client)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Junior Python Developer")
        self.assertEqual(result[0]["salary_from"], 80000)
        self.assertEqual(result[0]["snippet"], "Python, Django")  # HTML stripped
        self.assertIsNotNone(result[0]["published_at"])


class VacancyListViewTests(TestCase):
    def test_shows_vacancies(self):
        Vacancy.objects.create(external_id="1", title="Junior Python",
                               company="X", url="https://hh.ru/vacancy/1")
        response = self.client.get(reverse("vacancy-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Junior Python")

    def test_empty_state(self):
        response = self.client.get(reverse("vacancy-list"))
        self.assertEqual(response.status_code, 200)