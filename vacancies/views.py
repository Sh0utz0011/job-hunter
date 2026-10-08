from django.db.models import Avg, Count, Q
from django.views.generic import ListView

from .models import Vacancy


class VacancyListView(ListView):
    model = Vacancy
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Vacancy.objects.all()

        context["total"] = qs.count()
        context["with_salary"] = qs.filter(
            Q(salary_from__isnull=False) | Q(salary_to__isnull=False)
        ).count()

        # Средняя "вилка" по вакансиям с зарплатой
        avg_from = qs.filter(salary_from__isnull=False).aggregate(a=Avg("salary_from"))["a"]
        avg_to = qs.filter(salary_to__isnull=False).aggregate(a=Avg("salary_to"))["a"]
        context["avg_salary"] = f"{int(avg_from or 0):,}–{int(avg_to or 0):,} ₽" if (avg_from or avg_to) else "—"

        # Топ городов
        context["top_cities"] = (
            qs.exclude(area_name="")
            .values("area_name")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        # Простой поиск по ?q=...
        q = self.request.GET.get("q", "").strip()
        if q:
            context["vacancies"] = context["vacancies"].filter(
                Q(title__icontains=q) | Q(company__icontains=q) | Q(snippet__icontains=q)
            )
            context["query"] = q

        return context