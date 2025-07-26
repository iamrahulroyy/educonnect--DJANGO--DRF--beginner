from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='register'),
]
