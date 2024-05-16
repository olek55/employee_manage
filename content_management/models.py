from django.db import models
from markdownx.models import MarkdownxField

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownxField()
    summary = models.TextField()
    meta_description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to='author_images/')

    def __str__(self):
        return self.name