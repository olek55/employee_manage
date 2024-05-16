from country_management.models import TaxObligations, Country
import concurrent.futures
from django.core.management.base import BaseCommand
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_openai import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


class Command(BaseCommand):
    help = 'Updates TaxObligations for each country'

    def get_employer_tax_responsibilites(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        tools = [
            tavily_tool
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Generate a Markdown-formatted answer. Your answer start with H2 headings and use H3, H4 if needed. Don't create table of contents. Don't include H1 heading in your response "),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, model_kwargs={"response_format": {"type": "json_object"}})
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the employer tax responsibilities in {country.name}. Ensure authoritative resources are integrated within the guide to provide verification. Only return the guide."})
        return response["output"]



    def get_employee_tax_deductions(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        tools = [
            tavily_tool
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Generate a Markdown-formatted answer. Your answer start with H2 headings and use H3, H4 if needed. Don't create table of contents. Don't include H1 heading in your response "),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, model_kwargs={"response_format": {"type": "json_object"}})
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the employee tax deductions in {country.name}. Embed relevant references within the text to enhance credibility.  Only return the guide."})
        return response["output"]


    def get_vat(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        tools = [
            tavily_tool
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Generate a Markdown-formatted answer. Your answer start with H2 headings and use H3, H4 if needed. Don't create table of contents. Don't include H1 heading in your response "),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, model_kwargs={"response_format": {"type": "json_object"}})
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted  the Value-Added Tax (VAT) implications for services in {country.name}. Integrate authoritative sources directly into the content for substantiation. Only return the guide."})
        return response["output"]


    def get_tax_incentives(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        tools = [
            tavily_tool
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Generate a Markdown-formatted answer. Your answer start with H2 headings and use H3, H4 if needed. Don't create table of contents. Don't include H1 heading in your response "),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, model_kwargs={"response_format": {"type": "json_object"}})
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the tax incentives available to businesses in {country.name}. Incorporate relevant sources within the guide for factual accuracy.  Only return the guide."})
        return response["output"]


    def update_or_create_taxObligations(self, country):
        employer_tax_responsibilites = self.get_employer_tax_responsibilites(country)
        employee_tax_deductions = self.get_employee_tax_deductions(country)
        vat = self.get_vat(country)
        tax_incentives = self.get_tax_incentives(country)
        try:
            taxObligation, created = TaxObligations.objects.update_or_create(
                country=country,
                defaults={
                    'employer_tax_responsibilites': employer_tax_responsibilites,
                    "employee_tax_deductions": employee_tax_deductions,
                    "vat": vat,
                    "tax_incentives": tax_incentives
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created TaxObligation entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated TaxObligation for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating TaxObligation for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.filter(name='Ireland')
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_taxObligations, country) for country in countries]
            concurrent.futures.wait(futures)