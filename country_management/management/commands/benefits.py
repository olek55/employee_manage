from django.core.management.base import BaseCommand
from country_management.models import Benefit, Country
from openai import OpenAI
import concurrent.futures
import json

class Command(BaseCommand):
    help = 'Generates and associates leave types with detailed descriptions for each country'

    def fetch_leave_types(self, country):
        client = OpenAI()  # Instantiate your OpenAI client
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert in local laws in all countries I mention. I'm writing content about employment in different countries. You output only in markdown."},
                {
                    "role": "user",
                    "content": f"I want to know the types of benefits that are available in {country.name}. Return in a list format like this: `benefits: []`. This is an example. If there are no benefits, return an empty list."
                }
            ],
            response_format={"type": "json_object"},  # Correcting the format based on the context
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        leave_types = json.loads(response.choices[0].message.content)['benefits']
        print(leave_types)
        return (country, leave_types)

    def fetch_leave_description(self, country, leave_type, leave_types):
        client = OpenAI()  # Assuming OpenAI client is correctly configured
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant, output markdown format in JSON."},
                {
                    "role": "user",
                    "content": f"Provide a detailed description for {leave_type} in {country.name}. The text is part of a list of benefits for this country, so keep that in mind when creating the description. So you don't have to start the description with mentioning the country. The rest of the benefits for this country: {leave_types}. The description should be made for employers that are looking to hire their workforce in {country.name}. Don't include titles or anything. Output in markdown. Output like this: `description: 'description'`."
                }
            ],
            response_format={"type": "json_object"},  # Correcting the format based on the context
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        description = json.loads(response.choices[0].message.content)['description']
        print(description)
        return description

    def update_country_leaves(self, country_leave_types_pair):
        country, leave_types = country_leave_types_pair
        if not leave_types:
            self.stdout.write(self.style.WARNING(f'No leave types found for {country.name}, skipping description fetching.'))
            return
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(leave_types)) as executor:
            future_to_description = {
                executor.submit(self.fetch_leave_description, country, leave_type, leave_types): leave_type
                for leave_type in leave_types
            }
            for future in concurrent.futures.as_completed(future_to_description):
                leave_type = future_to_description[future]
                try:
                    description = future.result()
                    leave, created = Benefit.objects.get_or_create(
                        country=country,
                        name=leave_type,
                        defaults={'description': description}
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully created {leave_type} with detailed description for {country.name}'))
                except Exception as exc:
                    self.stdout.write(self.style.ERROR(f'Error fetching description for {leave_type}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_country = {executor.submit(self.fetch_leave_types, country): country for country in countries}
            for future in concurrent.futures.as_completed(future_to_country):
                country_leave_types_pair = future.result()
                self.update_country_leaves(country_leave_types_pair)
