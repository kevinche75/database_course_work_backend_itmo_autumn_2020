from django.urls import path
from .views import book_ticket, get_business, get_price

urlpatterns = [
    path('', book_ticket),
    path('business/', get_business),
    path('price/', get_price)

]
