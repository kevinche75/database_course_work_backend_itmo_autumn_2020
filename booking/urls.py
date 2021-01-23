from django.urls import path
from .views import book_ticket

urlpatterns = [
    path('book/', book_ticket),
]
