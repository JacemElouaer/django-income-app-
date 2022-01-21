from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
# permission decorator
@login_required(login_url='authentication/login')
def index(request):
    Expenses = Expense.objects.all()
    context = {
        "Expenses": Expenses
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
    context = {
            "expense" :  expense
        }
    if request.method ==  "GET":

        return  render(request ,  'expenses/edit-expenses.html' , context)
    if request.method == "POST":

        messages.info(request , "Handling Edit ")

        return render(request, 'expenses/edit-expenses.html', context)
