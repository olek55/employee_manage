from django.core.management.base import BaseCommand
from content_management.models import Blog, Category, Author
import csv
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import html2text

class Command(BaseCommand):
    help = 'Load a blogs CSV file into the database and converts HTML in the content field to Markdown'

    def handle(self, *args, **options):
        converter = html2text.HTML2Text()
        converter.ignore_links = False  # Set to False if you want to convert URLs to Markdown links

        with open('content_management/management/commands/blogs.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category, _ = Category.objects.get_or_create(
                    name=row['Blog Category']
                )
                author = Author.objects.first()  # Assuming there is at least one author

                # Convert HTML content to Markdown
                markdown_content = converter.handle(row['Post Body'])

                # Assuming 'Main Image' column contains the URL to the image
                image_url = row['Main Image']
                image_path = None
                if image_url:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        folder_path = "blog_images/"
                        file_name = f"{folder_path}{row['Slug']}.jpg"
                        image_content = ContentFile(response.content)
                        image_path = default_storage.save(file_name, image_content)
                    else:
                        self.stdout.write(self.style.ERROR(f"Failed to download image for {row['Blog Title']} from {image_url}"))

                blog = Blog.objects.create(
                    title=row['Blog Title'],
                    content=markdown_content,  # Use the converted Markdown content
                    meta_description=row['Meta Description'],
                    slug=row['Slug'],
                    summary=row['Post Summary'],
                    author=author,
                    image=image_path,
                    created_at=row['Created On'],
                    updated_at=row['Updated On'],
                    category=category
                )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded and updated blog: "{blog.title}"'))
