from . import views
from .views import Home, Table
from django.urls import path

urlpatterns = [
    path('', Home.as_view()),#views.home, name='invoice-home'),
    path('table/', Table.as_view()),
    path('table/<login>/', Table.as_view()),#views.table, name='invoice-table'),
]
