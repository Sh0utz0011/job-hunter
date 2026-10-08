import re
from datetime import datetime

import httpx

HH_API_URL = "https://api.hh.ru/vacancies"
# Более "браузерный" User-Agent + обязательный Accept
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}


def _strip_html(text):
    return re.sub(r"<[^>]+>", "", text or "").strip()


def _parse_dt(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return None


def fetch_vacancies(query, area="", per_page=20, client=None):
    """Тянет вакансии с hh.ru и возвращает нормализованный список словарей."""
    own_client = client is None
    if own_client:
        client = httpx.Client(headers=HEADERS, timeout=15, follow_redirects=True)
    try:
        params = {"text": query, "per_page": per_page, "page": 0, "search_field": "name"}
        if area:
            params["area"] = area
        response = client.get(HH_API_URL, params=params)

        # Обработка ошибок
        if response.status_code == 403:
            print(f"⚠️ HH.ru вернул 403 для запроса '{query}'. Возможно, временная блокировка.")
            return []

        response.raise_for_status()
        items = response.json().get("items", [])
    finally:
        if own_client:
            client.close()

    result = []
    for item in items:
        salary = item.get("salary") or {}
        snippet = item.get("snippet") or {}
        result.append({
            "external_id": item["id"],
            "title": item.get("name", ""),
            "company": (item.get("employer") or {}).get("name", ""),
            "url": item.get("alternate_url") or f"https://hh.ru/vacancy/{item['id']}",
            "salary_from": salary.get("from"),
            "salary_to": salary.get("to"),
            "currency": salary.get("currency") or "",
            "area_name": (item.get("area") or {}).get("name", ""),
            "published_at": _parse_dt(item.get("published_at")),
            "snippet": _strip_html(snippet.get("requirement")) or _strip_html(snippet.get("responsibility")),
        })
    return result