from country_management.models import CulturalConsiderations, Country
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
    help = 'Updates CulturalConsiderations for each country'

    def get_communication_styles(self, country):

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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted guide to communication styles in workplaces within {country.name}. Cover aspects like directness, formality, and the interpretation of non-verbal cues. Incorporate insights from cultural studies and business practices into your analysis. Only return the guide."})
        return response["output"]

    def get_negotiation_practices(self, country):

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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted guide examining negotiation practices in {country.name}.  Delve into typical approaches, strategies, and the influence of cultural norms on business dealings.  Incorporate references from authoritative sources to strengthen the guide's credibility. Only return the guide."})
        return response["output"]

    def get_hierarchical_structures(self, country):

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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted guide exploring hierarchical structures in businesses within {country.name}. Cover the impact these structures have on decision-making, team dynamics, and leadership styles. Weave in insights from cultural analysis and management theories as you write the guide. Only return the guide."})
        return response["output"]

    def get_holidays_and_observances(self, country):

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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted guide to major holidays and observances in {country.name} that affect business operations. Include statutory holidays, regional observances, and their impact on work schedules. Incorporate cultural and legal notes where relevant. Only return the guide."})
        return response["output"]

    def update_or_create_cultural_considerations(self, country):
        communication = self.get_communication_styles(country)
        negotiation = self.get_negotiation_practices(country)
        hierarchy = self.get_hierarchical_structures(country)
        holidays = self.get_holidays_and_observances(country)

        try:
            culturalConsideration, created = CulturalConsiderations.objects.update_or_create(
                country=country,
                defaults={
                    'communication_styles_in_the_workplace': communication,
                    "negotiation_practices": negotiation,
                    "understanding_hierarchical_structures": hierarchy,
                    "holidays_and_observances_affecting_business_operations": holidays
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created CulturalConsiderations entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated CulturalConsiderations for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating CulturalConsiderations for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_cultural_considerations, country) for country in countries]
            concurrent.futures.wait(futures)
