from country_management.models import HealthandSafetyRequirements, Country
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
    help = 'Updates HealthandSafetyRequirements for each country'

    def get_health_and_safety_laws(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, max_tokens=2000, )
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        tools = [
            tavily_tool
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You are a helpful assistant. Generate a Markdown-formatted answer. Your answer start with H2 headings and use H3, H4 if needed. Don't create table of contents. Don't include H1 heading in your response "),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                                       model_kwargs={"response_format": {"type": "json_object"}})
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted an in-depth overview of health and safety laws in {country.name}. Embed relevant legal references within the text for accuracy.  Only return the guide."})
        return response["output"]


    def get_occupational_health_and_safety(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the standards and practices for occupational health and safety in {country.name}. Incorporate authoritative sources directly into the content for substantiation. Only return the guide."})
        return response["output"]


    def get_workplace_inspections(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.8, max_tokens=2000, )
        search = TavilySearchAPIWrapper()
        tavily_tool = TavilySearchResults(api_wrapper=search)
        tools = [
            tavily_tool
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You are a helpful assistant. Generate a Markdown-formatted answer. Your answer start with H2 headings and use H3, H4 if needed. Don't create table of contents. Don't include H1 heading in your response "),
                MessagesPlaceholder("chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                                       model_kwargs={"response_format": {"type": "json_object"}})
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted  Only the role and procedures for workplace inspections in {country.name}, highlighting inspection criteria, frequency, and follow-up actions. Seamlessly integrate relevant regulations and guidelines within the guide.  return the guide."})
        return response["output"]


    def get_workplace_accidents(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the protocols for dealing with workplace accidents in {country.name}, including reporting requirements, investigation processes, and compensation claims. Embed credible legal and regulatory references to support the discussion Only return the guide."})
        return response["output"]


    def update_or_create_health_and_safety(self, country):
        health_safety_laws = self.get_health_and_safety_laws(country)
        occupational_health = self.get_occupational_health_and_safety(country)
        workplace_inspections = self.get_workplace_inspections(country)
        workplace_accidents = self.get_workplace_accidents(country)

        try:
            hsRequirements, created = HealthandSafetyRequirements.objects.update_or_create(
                country=country,
                defaults={
                    'health_and_safety_laws': health_safety_laws,
                    "occupational_health_and_safety": occupational_health,
                    "workplace_inspection": workplace_inspections,
                    "workplace_accidents": workplace_accidents
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created HealthandSafetyRequirements entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated HealthandSafetyRequirements for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating HealthandSafetyRequirements for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_health_and_safety, country) for country in countries]
            concurrent.futures.wait(futures)
