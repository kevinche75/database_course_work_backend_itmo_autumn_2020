from django.urls import path
from .views import book_ticket, get_business

urlpatterns = [
    path('', book_ticket),
    path('business/', get_business)
]
