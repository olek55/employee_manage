from country_management.models import WorkersRightsandProtections, Country
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
    help = 'Updates WorkersRightsandProtections for each country'

    def get_termination_regulations(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted into the regulations surrounding the termination of employment in {country.name}, covering lawful grounds for dismissal, notice requirements, and severance pay. Ensure that authoritative resources are integrated within the text to support your discussion. Only return the guide."})
        return response["output"]


    def get_discrimination_laws(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the anti-discrimination laws in {country.name}, focusing on protected characteristics, redress mechanisms, and employer responsibilities. Embed credible sources directly into the content for validation. Only return the guide."})
        return response["output"]


    def get_working_conditions(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the standards for working conditions in {country.name}, including work hours, rest periods, and ergonomic requirements. Incorporate relevant references within the guide to enhance reliability. Only return the guide."})
        return response["output"]


    def get_health_and_safety_regulations(self, country):
        llm = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.5, max_tokens=2000, )
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted health and safety regulations in the workplace in {country.name}, discussing employer obligations, employee rights, and enforcement agencies. Seamlessly integrate authoritative sources to substantiate the information. Only return the guide."})
        return response["output"]



    def update_or_create_worker_rights(self, country):
        termination_regulations = self.get_termination_regulations(country)
        discrimination_laws = self.get_discrimination_laws(country)
        working_conditions = self.get_working_conditions(country)
        health_and_safety_regulations = self.get_health_and_safety_regulations(country)

        try:
            workerRights, created = WorkersRightsandProtections.objects.update_or_create(
                country=country,
                defaults={
                    'termination': termination_regulations,
                    "discrimination": discrimination_laws,
                    "working_conditions": working_conditions,
                    "health_and_safety": health_and_safety_regulations
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created WorkersRightsandProtections entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated WorkersRightsandProtections for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating WorkersRightsandProtections for {country.name}: {exc}'))

    # ... (handle method)


    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_worker_rights, country) for country in countries]
            concurrent.futures.wait(futures)
