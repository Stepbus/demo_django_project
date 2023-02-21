from django.urls import path

from . import views

urlpatterns = [
    path('shop/', views.home, name='shop'),
    path('basket/<id>/', views.ShowBasket.as_view(), name='basket'),
    path('backpack-list/', views.CreateShoppingList.as_view(), name='backpack-list'),
    path('shopping-list/', views.ShowShoppingList.as_view(), name='shopping-list'),
    path('delete/<product_id>/', views.DeleteFromBackpack.as_view(), name='delete'),
    path('notebook/', views.NotebookList.as_view(), name='notebook'),
    path('dishwasher/', views.DishwasherList.as_view(), name='dishwasher'),
    path('vacuum-cleaner/', views.VacuumCleanerList.as_view(), name='vacuumCleaner'),
    path('tv/', views.TVList.as_view(), name='tv'),
    path('detail-product/<pk>/', views.DetailViewProduct.as_view(), name='detail-product'),
    # path('add-product/<product_id>/', views.AddProductsInBackpack.as_view(), name='add_product'),
    ]
