
from django.contrib import admin
from django.urls import path
from  .views import *
from  django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='incomes'),
    path('add-incomes', add_incomes, name='add-incomes'),
    path('edit-incomes/<int:id>', edit_incomes, name='edit-incomes'),
    path('delete_incomes/<int:id>', delete_income, name='delete-incomes'),
    path('search_incomes', csrf_exempt(search_income), name='search_incomes')
]
