from django.shortcuts import render
from rest_framework import generics
from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer
from rest_framework.permissions import AllowAny

class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by('-updated_at')
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['title', 'id', 'updated_at']  # Specify which fields can be ordered against
    ordering = ['title']  # Set the default ordering
    

class LatestBlogsView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by('-updated_at')[:3]
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]

class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all().order_by('-updated_at')
    serializer_class = BlogDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'  # Set the field to look up against