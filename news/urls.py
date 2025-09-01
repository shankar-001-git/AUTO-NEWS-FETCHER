from django.urls import path
from .views import DashboardView, fetch_latest

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("fetch-latest/", fetch_latest, name="fetch_latest"),
]



