from django.urls import path
from .views import auth, get_schedule

urlpatterns = [
    path('', auth),
    path('schedule/', get_schedule)
]