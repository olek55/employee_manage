from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from country_management.models import Country, Currency
import time
import pandas as pd
import requests
from io import BytesIO
    
class Command(BaseCommand):
    help = 'Add countries'

    def handle(self, *args, **kwargs):
        countries = pd.read_csv('country_management/management/commands/Rivermate - Countries.csv')

        for index, row in countries.iterrows():
            print(row['Name'])
            currency, _ = Currency.objects.update_or_create(
                currency_code=row['Currency code'],
                currency_name=row['Currency name'],
                currency_symbol=row['Currency symbol'],
            )
            # Fetch and save the image
            image_url = row['Header image']  # Assuming 'Header image' column contains the URL to the image
            if image_url:  # Check if the URL is not empty
                response = requests.get(image_url)
                if response.status_code == 200:
                    folder_path = "country_images/"
                    # Create a name for your file. This example uses the country name plus ".jpg"
                    file_name = f"{folder_path}{row['Slug']}.jpg"
                    # Create a ContentFile for the image
                    image_content = ContentFile(response.content)
                    # Save the image to the ImageField
                    image_path = default_storage.save(file_name, image_content)
                else:
                    print(f"Failed to download image for {row['Name']} from {image_url}")
                    image_path = None
            else:
                image_path = None

            flag_url = row['Flag']  # Assuming 'Flag' column contains the URL to the flag image
            if flag_url:  # Check if the URL is not empty
                response = requests.get(flag_url)
                if response.status_code == 200:
                    folder_path = "country_flags/"
                    # Create a name for your file. This example uses the country name plus ".jpg"
                    file_name = f"{folder_path}{row['Slug']}.svg"
                    # Create a ContentFile for the image
                    flag_content = ContentFile(response.content)
                    # Save the image to the ImageField
                    flag_path = default_storage.save(file_name, flag_content)
                else:
                    print(f"Failed to download flag for {row['Name']} from {flag_url}")
                    flag_path = None

            country, created = Country.objects.update_or_create(
                slug=row['Slug'],
                defaults={
                    'name': row['Name'],
                    'flag': flag_path,
                    'capital': row['Capital'],
                    'region': row['Region'],
                    'population': row['Population'],
                    'gdp_growth': row['Gdp growth'],
                    'gdp_share': row['World gdp share'],
                    'currency': currency,
                    'image': image_path,
                    'holiday_code': row['Public holidays id'],
                    'language': row['Language'],
                    'availability': row['Available?'],
                }
            )

            print(f"{country} {'created' if created else 'updated'}")

            print(f"{country} {'created' if created else 'updated'}")
