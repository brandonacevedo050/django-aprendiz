from django.urls import path

from .views import AprendizDetailView, AprendizListCreateView

urlpatterns = [
    path("", AprendizListCreateView.as_view(), name="aprendiz-list-create"),
    path("<int:id>/", AprendizDetailView.as_view(), name="aprendiz-detail"),
]
