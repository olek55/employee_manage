from country_management.models import Payment
import concurrent.futures
from django.core.management.base import BaseCommand
from country_management.models import Country
import concurrent.futures
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


class Command(BaseCommand):
    help = 'Updates minimum wage for each country in the Payment model'

    def fetch_minimum_wage(self, country):
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        agent_chain = initialize_agent(
            [tavily_tool],
            llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        # run the agent
        response = agent_chain.run(
            f"You are an expert in local laws in all countries I mention. I'm writing content about employment in different countries.Answer several sentences. You output only in markdown. Question: Minimum wage in {country.name} 2024",
        )
        return response

    def payroll_cycle(self, country):
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        agent_chain = initialize_agent(
            [tavily_tool],
            llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        # run the agent
        response = agent_chain.run(
            f"You are an expert in local laws in all countries I mention. I'm writing content about employment in different countries.Answer several sentences. You output only in markdown. Question: Payroll cycle in {country.name} 2024",
        )
        return response

    def frequency(self, country):
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)

        # initialize the agent
        agent_chain = initialize_agent(
            [tavily_tool],
            llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

        response = agent_chain.run(
            f"You are an expert in local laws in all countries I mention. I'm writing content about employment in different countries.Answer several sentences. You output only in markdown. Question: Payment frequency in {country.name} 2024. If you don't have information about 2024 provider earlier data",
        )
        return response

    def update_payment(self, country):
        minimum_wage = self.fetch_minimum_wage(country)
        payroll_cycle = self.payroll_cycle(country)
        frequency = self.frequency(country)
        try:
            payment, created = Payment.objects.update_or_create(
                country=country,
                defaults={
                    'minimum_wage': minimum_wage,
                    "frequency": frequency,
                    "payroll_cycle": payroll_cycle
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created minimum wage entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated minimum wage for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating payments for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        countries = countries[:1]
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(self.update_payment, country) for country in countries]
            concurrent.futures.wait(futures)
