from django.shortcuts import render, redirect
from .models import User, Expense, Income, Budget
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'finances/login.html', {'error': 'Nome ou senha inválidos'})
    return render(request, 'finances/login.html')

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'finances/dashboard.html', {
        'expenses': expenses,
        'incomes': incomes,
        'budgets': budgets
    })

@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'success': False, 'error': 'Usuário ou senha incorretos'}, status=401)