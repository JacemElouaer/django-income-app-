
from django.contrib import admin
from django.urls import path
from  .views import *

urlpatterns = [
    path('', index, name='expenses'),
    path('add-expenses', add_expenses, name='add-expenses'),
    path('edit-expense', edit_expenses, name='edit-expenses'),

]
