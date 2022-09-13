from django.urls import path, include
from products import views

urlpatterns = [
    path('user_creation', views.register, name= 'user_creation'),
    path('user_login', views.login, name= 'user_login'),
    path('product_save', views.product_save, name= 'product_save'),
    path('product_list', views.product_list, name= 'product_list'),
    path('product_update', views.product_update, name= 'product_update'),
    path('product_delete', views.product_delete, name= 'product_delete'),
]