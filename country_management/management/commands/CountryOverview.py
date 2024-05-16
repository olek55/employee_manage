from country_management.models import CountryOverview, Country
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
    help = 'Updates CountryOverview for each country'

    def get_country_description(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted an in-depth overview of {country.name}, covering geographical, historical, and socio-economic aspects. Integrate authoritative sources directly into the narrative to support your descriptions.  Only return the guide."})
        return response["output"]


    def get_workforce_description(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the characteristics of the workforce in {country.name}, including demographics, skill levels, and sectoral distribution. Embed relevant statistics and findings from credible sources within the content.  Only return the guide."})
        return response["output"]

    def get_cultural_norms(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the cultural norms in {country.name} that influence employment practices, including work-life balance, communication styles, and organizational hierarchies. Incorporate insights from reputable sources to enrich the guide. Only return the guide."})
        return response["output"]


    def get_key_industries(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the key industries and employment sectors driving the economy in {country.name}, highlighting emerging sectors and those with significant employment. Include up-to-date references within the text to substantiate your points. Only return the guide."})
        return response["output"]


    def update_or_create_country_overview(self, country):
        description = self.get_country_description(country)
        workforce = self.get_workforce_description(country)
        cultural_norms = self.get_cultural_norms(country)
        industries = self.get_key_industries(country)

        try:
            overview, created = CountryOverview.objects.update_or_create(
                country=country,
                defaults={
                    'country_description': description,
                    "workforce_description": workforce,
                    "cultural_norms_impacting_employment": cultural_norms,
                    "key_industries_and_employment_sectors": industries
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created CountryOverview entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated CountryOverview for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating CountryOverview for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_country_overview, country) for country in countries]
            concurrent.futures.wait(futures)
