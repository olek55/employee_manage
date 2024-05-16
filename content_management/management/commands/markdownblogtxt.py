from django.core.management.base import BaseCommand
from content_management.models import Blog
import html2text

class Command(BaseCommand):
    help = 'Converts HTML in the content field to Markdown and stores it in content2'

    def handle(self, *args, **kwargs):
        converter = html2text.HTML2Text()
        converter.ignore_links = False  # Set to True if you want to ignore converting URLs to Markdown links
        blogs = Blog.objects.all()

        for blog in blogs:
            markdown_content = converter.handle(blog.content)
            blog.content2 = markdown_content
            blog.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully converted and updated blog: "{blog.title}"'))
