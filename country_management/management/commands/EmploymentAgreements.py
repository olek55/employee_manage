from country_management.models import EmploymentAgreements, Country
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
    help = 'Updates EmploymentAgreements for each country'

    def get_employment_agreement_types(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the various types of employment agreements in {country.name}. Integrate relevant legal sources within the text to provide accuracy. Only return the guide."})
        return response["output"]


    def get_essential_clauses(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the essential clauses that should be included in employment agreements in {country.name}. Embed authoritative references to support the discussion. Only return the guide."})
        return response["output"]


    def get_probationary_period(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted  the concept of the probationary period in employment agreements in {country.name}. Incorporate credible sources directly into the guide for validation. Only return the guide."})
        return response["output"]


    def get_confidentiality_and_non_compete(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted  the confidentiality and non-compete clauses in employment agreements in {country.name}. Seamlessly integrate relevant legal sources within the text. Only return the guide."})
        return response["output"]


    def update_or_create_employment_agreements(self, country):
        types = self.get_employment_agreement_types(country)
        clauses = self.get_essential_clauses(country)
        probation = self.get_probationary_period(country)
        confidentiality = self.get_confidentiality_and_non_compete(country)

        try:
            empAgreements, created = EmploymentAgreements.objects.update_or_create(
                country=country,
                defaults={
                    'types_of_employment_agreements': types,
                    "essential_clauses": clauses,
                    "probationary_period": probation,
                    "confidentiality_and_non_compete_clauses": confidentiality,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created EmploymentAgreements entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated EmploymentAgreements for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating EmploymentAgreements for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_employment_agreements, country) for country in countries]
            concurrent.futures.wait(futures)
