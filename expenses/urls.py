
from django.contrib import admin
from django.urls import path
from  .views import *
from  django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='expenses'),
    path('add-expenses', add_expenses, name='add-expenses'),
    path('edit-expense/<int:id>', edit_expenses, name='edit-expenses'),
    path('delete_expenses/<int:id>', delete_expenses, name='delete-expenses'),
    path('search_expenses', csrf_exempt(search_expenses), name='search_expenses')
]
