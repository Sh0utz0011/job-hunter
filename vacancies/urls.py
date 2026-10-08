from django.urls import path
from .views import VacancyListView

urlpatterns = [path("", VacancyListView.as_view(), name="vacancy-list")]