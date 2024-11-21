from django.urls import path, views
from .views import signup_view, login_view, logout_view, item_list, item_create, item_delete

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('items/', item_list, name='item_list'),
    path('items/create/', item_create, name='item_create'),
    path('items/delete/<int:pk>/', item_delete, name='item_delete'),
]
