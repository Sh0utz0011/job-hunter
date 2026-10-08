from django.contrib import admin
from .models import SearchQuery, Vacancy


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("text", "area", "is_active")
    list_editable = ("is_active",)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "salary_display", "area_name", "published_at")
    search_fields = ("title", "company")