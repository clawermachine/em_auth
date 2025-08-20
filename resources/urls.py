from django.urls import path
from .views import resource_action

urlpatterns = [
    path("<str:resource>/", resource_action, name="resource_view"),
]
