from django.urls import path, include
from catalog.views import (ContactsTemplateView, ProductListView, ProductDetailView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView)
from .views import CategoryListView
from django.urls import path
from django.views.decorators.cache import cache_page

app_name = 'catalog'  # Добавление пространства имен для приложения

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('users/', include('users.urls')),
    path('categories/', CategoryListView.as_view(), name='category_list')
]
