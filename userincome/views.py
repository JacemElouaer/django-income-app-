from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.http import JsonResponse
import json


# Create your views here.


@login_required(login_url='authentication/login')
def index(request):
    # paginator need
    # 1 /  declaration
    # 2 / get page number from  request GET
    # 3 / pass the page_obj in the context
    incomes = Income.objects.all()
    sources = Source.objects.all()
    paginator = Paginator(incomes, 4)
    # this means that paginator will devide incomes on 2
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = "{currency}"
    context = {
        "incomes": incomes,
        "page_obj": page_obj,
        "currency": currency
    }
    print(incomes)
    return render(request, 'income/index.html', context)


def add_incomes(request):
    sources = Source.objects.all()
    context = {
        "sources": sources,
        "Values": request.POST
    }
    if request.method == "GET":
        return render(request, 'income/add_incomes.html', context)
    if request.method == "POST":
        Sources = request.POST['source']
        Expense_date = request.POST['income_date']
        Description = request.POST['description']
        Amount = request.POST['amount']
        if not Amount:
            messages.error(request, "Amount is required ")
            return render(request, 'income/add_incomes.html', context)
        if not Description:
            messages.error(request, "Description is required ")
            return render(request, 'income/add_incomes.html', context)
        if not Expense_date:
            messages.error(request, "Income_date is required ")
            return render(request, 'income/add_incomes.html', context)
        if not Sources:
            messages.error(request, "Source is required ")
            return render(request, 'income/add_incomes.html', context)

        Income.objects.create(owner=request.user, amount=Amount, date=Expense_date, source=Sources,
                              description=Description)
        messages.success(request, "income is added successfully  ! ")
        return redirect('incomes')


def edit_incomes(request, id):
    income = Income.objects.get(id=id)
    sources = Source.objects.all()
    context = {
        "income": income,
        "sources": sources
    }
    if request.method == "GET":
        return render(request, 'income/edit_incomes.html', context)
    if request.method == "POST":
        messages.info(request, "Handling Edit ")
        Sources = request.POST['source']
        Expense_date = request.POST['income_date']
        Description = request.POST['description']
        Amount = request.POST['amount']
        if not Amount:
            messages.error(request, "Amount is required ")
            return render(request, 'income/edit_incomes.html', context)
        if not Description:
            messages.error(request, "Description is required ")
            return render(request, 'income/edit_incomes.html', context)
        if not Expense_date:
            messages.error(request, "Income_date is required ")
            return render(request, 'income/edit_incomes.html', context)
        if not Sources:
            messages.error(request, "Source is required ")
            return render(request, 'income/edit_incomes.html', context)

        income.amount = Amount
        income.date = Expense_date
        income.source = Sources
        income.description = Description
        income.save()
        messages.success(request, "Incomes updated successfully  ! ")
        return redirect('incomes')


def delete_income(request, id):
    income = Income.objects.get(id=id)
    income.delete()
    messages.success(request, "income Deleted successefully ! ! ")
    return redirect('incomes')


def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchIncomeText')
        expenses = Income.objects.filter(amount__istartswith=search_str,
                                         owner=request.user) \
                   | Income.objects.filter(date__istartswith=search_str,
                                           owner=request.user) \
                   | Income.objects.filter(description__icontains=search_str,
                                           owner=request.user) \
                   | Income.objects.filter(source__icontains=search_str,
                                           owner=request.user)

        search_str = json.loads(request.body).get('searchText')
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
