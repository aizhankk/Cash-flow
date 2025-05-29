from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.cashflow_create, name='cashflow_create'),
    path('edit/<int:pk>/', views.cashflow_edit, name='cashflow_edit'),
    path('delete/<int:pk>/', views.cashflow_delete, name='cashflow_delete'),
    path('directory/', views.directory, name='directory'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('status/edit/<int:pk>/', views.status_edit, name='status_edit'),
    path('type/edit/<int:pk>/', views.type_edit, name='type_edit'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('subcategory/edit/<int:pk>/', views.subcategory_edit, name='subcategory_edit'),
    path('status/delete/<int:pk>/', views.status_delete, name='status_delete'),
    path('type/delete/<int:pk>/', views.type_delete, name='type_delete'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),
]