from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, ItemForm
from .models import Item

def home_view(request):
    return render(request, 'users/base.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('item_list')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def item_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    items = Item.objects.filter(user=request.user)
    return render(request, 'users/item_list.html', {'items': items})

def item_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'users/item_form.html', {'form': form})

def edit_view(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item) 

    return render(request, 'users/item_edit.html', {'form': form, 'item': item})

def item_delete(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    item = Item.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'users/item_delete.html', {'item': item})
