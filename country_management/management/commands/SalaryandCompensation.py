from country_management.models import SalaryandCompensation, Country
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
    help = 'Updates SalaryandCompensation for each country'

    def get_market_competitive_salaries(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the concept of market competitive salaries in {country.name}. Integrate authoritative financial and employment resources within the content for substantiation. Only return the guide."})
        return response["output"]


    def get_minimum_wage(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the minimum wage regulations in {country.name}. Embed relevant legislative references to ensure accuracy.  Only return the guide."})
        return response["output"]


    def get_bonuses_and_allowances(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the variety of bonuses and allowances offered to employees in {country.name}. Incorporate credible sources directly into the guide for validation. Only return the guide."})
        return response["output"]


    def get_payroll_cycle(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the payroll cycle practices in {country.name}. Seamlessly integrate authoritative financial and legal references within the text. Only return the guide."})
        return response["output"]


    def update_or_create_salary_and_compensation(self, country):
        market_analysis = self.get_market_competitive_salaries(country)
        min_wage = self.get_minimum_wage(country)
        bonuses = self.get_bonuses_and_allowances(country)
        payroll = self.get_payroll_cycle(country)

        try:
            salaryComp, created = SalaryandCompensation.objects.update_or_create(
                country=country,
                defaults={
                    'market_competitive_salaries': market_analysis,
                    "minimum_wage": min_wage,
                    "bonuses_and_allowances": bonuses,
                    "payroll_cycle": payroll
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created SalaryandCompensation entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated SalaryandCompensation for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating SalaryandCompensation for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_salary_and_compensation, country) for country in countries]
            concurrent.futures.wait(futures)
