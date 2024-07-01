from django.urls import path
from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('update/<slug:slug>', BlogUpdateView.as_view(), name='update'),
    path('view/<slug:slug>', BlogDetailView.as_view(), name='view'),
    path('delete/<slug:slug>/', BlogDeleteView.as_view(), name='delete')

]