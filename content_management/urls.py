from django.urls import path
from .views import BlogListView, BlogDetailView, LatestBlogsView

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('latest-blogs/', LatestBlogsView.as_view(), name='latest-blog-list'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='country-detail'),
]
