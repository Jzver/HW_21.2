from django.urls import path, include
from catalog.views import (ContactsTemplateView, ProductListView, ProductDetailView,
                           ProductCreateView, ProductUpdateView, ProductDeleteView)

app_name = 'catalog'  # Добавление пространства имен для приложения

urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),  # Изменено с 'create' на 'product_create'
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),  # Изменено с 'update' на 'product_update'
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),  # Изменено с 'delete' на 'product_delete'
    path('users/', include('users.urls')),
]
