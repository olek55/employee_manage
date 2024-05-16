from country_management.models import FreelancingandIndependentContracting, Country
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
    help = 'Updates FreelancingandIndependentContracting policies for each country'

    def get_employee_vs_contractor(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the legal distinctions between employees and independent contractors in {country.name}. Integrate relevant legal references within the text to ensure accuracy. Only return the guide."})
        return response["output"]


    def get_independent_contracting_practices(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted  the nuances of independent contracting in {country.name}, including contract structures, negotiation practices, and common industries. Embed authoritative sources to substantiate the discussion. Only return the guide."})
        return response["output"]


    def get_intellectual_property(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted intellectual property rights considerations for freelancers and independent contractors in {country.name}. Incorporate credible legal sources directly into the text for validation.  Only return the guide."})
        return response["output"]


    def get_tax_and_insurance(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the tax obligations and insurance options for freelancers and independent contractors in {country.name}. Seamlessly integrate relevant tax legislation and insurance norms within the guide. Only return the guide."})
        return response["output"]


    def update_or_create_freelancing(self, country):
        employee_vs_contractor = self.get_employee_vs_contractor(country)
        contracting = self.get_independent_contracting_practices(country)
        ip_rights = self.get_intellectual_property(country)
        tax_insurance = self.get_tax_and_insurance(country)

        try:
            freelanceInfo, created = FreelancingandIndependentContracting.objects.update_or_create(
                country=country,
                defaults={
                    'difference_employees_and_contractors': employee_vs_contractor,
                    "independent_contracting": contracting,
                    "intellectual_property_rights": ip_rights,
                    "tax_and_insurance": tax_insurance
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created FreelancingandIndependentContracting entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated FreelancingandIndependentContracting for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating FreelancingandIndependentContracting for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_freelancing, country) for country in countries]
            concurrent.futures.wait(futures)
