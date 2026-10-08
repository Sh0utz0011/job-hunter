from django.db import models


class SearchQuery(models.Model):
    """Настройки поиска: что и где ищем."""
    text = models.CharField(max_length=200, default="python")
    area = models.CharField(max_length=20, blank=True, default="",
                            help_text="ID региона hh.ru, пусто — вся Россия")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.text} (area={self.area or 'all'})"


class Vacancy(models.Model):
    """Вакансия, загруженная из hh.ru."""
    external_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=300)
    url = models.URLField(max_length=500)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10, blank=True, default="")
    area_name = models.CharField(max_length=200, blank=True, default="")
    published_at = models.DateTimeField(null=True, blank=True)
    snippet = models.TextField(blank=True, default="")
    fetched_at = models.DateTimeField(auto_now=True)
    is_new = models.BooleanField(default=True)  # флаг для Telegram-уведомлений

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.title} — {self.company}"

    @property
    def salary_display(self):
        if self.salary_from and self.salary_to:
            return f"{self.salary_from:,}–{self.salary_to:,} {self.currency}"
        if self.salary_from:
            return f"от {self.salary_from:,} {self.currency}"
        if self.salary_to:
            return f"до {self.salary_to:,} {self.currency}"
        return "з/п не указана"