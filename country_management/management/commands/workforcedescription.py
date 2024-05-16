from django.core.management.base import BaseCommand
from country_management.models import Country
from openai import OpenAI
import concurrent.futures

class Command(BaseCommand):
    help = 'Generates workforce descriptions for each country'

    def fetch_description(self, country):
        client = OpenAI()  # Instantiate your OpenAI client

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "user",
                    "content": f"Write a short description about the country {country.name}. The text should be made for employers that are looking to hire their workforce in {country.name}. Don't include titles or anything. Make sure to use a line break after a paragraph. Dont add a conclusion."
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        description = response.choices[0].message.content
        print(description)

        # You might want to handle DB operations separately to ensure thread safety
        return (country, description)

    def update_country_description(self, country_description_pair):
        country, description = country_description_pair
        country.workforce_description = description
        country.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated workforce description for {country.name}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all().filter(workforce_description__isnull=True)

        # Use ThreadPoolExecutor to fetch descriptions in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            # Map each country to the fetch_description function
            future_to_country = {executor.submit(self.fetch_description, country): country for country in countries}
            for future in concurrent.futures.as_completed(future_to_country):
                country_description_pair = future.result()
                self.update_country_description(country_description_pair)
