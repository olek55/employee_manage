from rest_framework import serializers
from .models import Blog, Author, Category

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'image']  # Add the fields you want to include

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']  # Add the fields you want to include

class BlogListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    # This serializer is for the list view
    class Meta:
        model = Blog
        fields = ['title', 'summary', 'slug', 'image', 'updated_at', 'category', 'author']



class BlogDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['title', 'summary', 'content', 'slug', 'image', 'updated_at', 'category', 'author']