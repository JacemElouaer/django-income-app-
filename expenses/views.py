from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreferences


# ==> table format


# Create your views here.
# permission decorator
@login_required(login_url='authentication/login')
def index(request):
    # paginator need
    # 1 /  declaration
    # 2 / get page number from  request GET
    # 3 / pass the page_obj in the context
    Expenses = Expense.objects.all()
    paginator = Paginator(Expenses, 4)
    # this means that paginator will devide expenses on 2
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreferences.objects.get(user=request.user).currency
    except UserPreferences.DoesNotExist:
        currency = "{currency}"
    context = {
        "Expenses": Expenses,
        "page_obj": page_obj,
        "currency":  currency
    }
    return render(request, 'expenses/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "Values": request.POST
    }
    if request.method == "GET":
        return render(request, 'expenses/add_expenses.html', context)
    if request.method == "POST":
        Categories = request.POST['category']
        Expense_date = request.POST['expense_date']
        Description = request.POST['description']
        Amount = request.POST['amount']
        if not Amount:
            messages.error(request, "Amount is required ")
            return render(request, 'expenses/add_expenses.html', context)
        if not Description:
            messages.error(request, "Description is required ")
            return render(request, 'expenses/add_expenses.html', context)
        if not Expense_date:
            messages.error(request, "Expense_date is required ")
            return render(request, 'expenses/add_expenses.html', context)
        if not Categories:
            messages.error(request, "Expense_date is required ")
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(owner=request.user, amount=Amount, date=Expense_date, category=Categories,
                               description=Description)
        messages.success(request, "Expense is added successfully  ! ")
        return redirect('expenses')


def edit_expenses(request, id):
    expense = Expense.objects.get(id=id)
    categories = Category.objects.all()
    context = {
        "expense": expense,
        "categories": categories
    }
    if request.method == "GET":
        return render(request, 'expenses/edit_expenses.html', context)
    if request.method == "POST":
        messages.info(request, "Handling Edit ")
        Categories = request.POST['category']
        Expense_date = request.POST['expense_date']
        Description = request.POST['description']
        Amount = request.POST['amount']
        if not Amount:
            messages.error(request, "Amount is required ")
            return render(request, 'expenses/edit_expenses.html', context)
        if not Description:
            messages.error(request, "Description is required ")
            return render(request, 'expenses/edit_expenses.html', context)
        if not Expense_date:
            messages.error(request, "Expense_date is required ")
            return render(request, 'expenses/edit_expenses.html', context)
        if not Categories:
            messages.error(request, "Category is required ")
            return render(request, 'expenses/edit_expenses.html', context)

        expense.amount = Amount
        expense.date = Expense_date
        expense.category = Categories
        expense.description = Description
        expense.save()
        messages.success(request, "Expense updated successfully  ! ")
        return redirect('expenses')


def delete_expenses(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    messages.success(request, "expense Deleted successefully")
    return redirect('expenses')


def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str,
                                          owner=request.user) \
                   | Expense.objects.filter(date__istartswith=search_str,
                                            owner=request.user) \
                   | Expense.objects.filter(description__icontains=search_str,
                                            owner=request.user) \
                   | Expense.objects.filter(category__icontains=search_str,
                                            owner=request.user)

        search_str = json.loads(request.body).get('searchText')
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
