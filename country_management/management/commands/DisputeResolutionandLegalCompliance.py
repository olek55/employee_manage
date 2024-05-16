from country_management.models import DisputeResolutionandLegalCompliance, Country
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
    help = 'Updates DisputeResolutionandLegalCompliance for each country'

    def get_labor_courts_and_arbitration(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the structure and function of labor courts and arbitration panels in {country.name}, including their jurisdiction, process, and typical cases handled. Integrate relevant legal sources to provide a comprehensive overview. Only return the guide."})
        return response["output"]


    def get_compliance_and_inspections(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the procedures and importance of compliance audits and inspections in {country.name}, covering who conducts them, frequency, and the consequences of non-compliance. Embed authoritative references within the text to ensure accuracy. Only return the guide."})
        return response["output"]


    def get_reporting_and_whistleblower(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted the mechanisms for reporting violations and the protections in place for whistleblowers in {country.name}, highlighting legal provisions and practical considerations. Incorporate credible legal and regulatory references directly into the guide for substantiation.Only return the guide."})
        return response["output"]


    def get_international_compliance(self, country):
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
        response = agent_executor.invoke({"input": f"Generate a Markdown-formatted how {country.name} complies with international labor standards, including adherence to conventions and treaties, and the impact on domestic labor laws. Seamlessly integrate relevant international and local legal sources within the text. Only return the guide."})
        return response["output"]


    def update_or_create_dispute_and_compliance(self, country):
        labor_courts = self.get_labor_courts_and_arbitration(country)
        compliance = self.get_compliance_and_inspections(country)
        reporting = self.get_reporting_and_whistleblower(country)
        international = self.get_international_compliance(country)

        try:
            legalCompliance, created = DisputeResolutionandLegalCompliance.objects.update_or_create(
                country=country,
                defaults={
                    'labor_courts_and_arbitration_panels': labor_courts,
                    "compliance_audits_and_inspections": compliance,
                    "reporting_and_whistleblower_protections": reporting,
                    "international_labor_standards_compliance": international
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created DisputeResolutionandLegalCompliance entry for {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated DisputeResolutionandLegalCompliance for {country.name}'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Error updating or creating DisputeResolutionandLegalCompliance for {country.name}: {exc}'))

    def handle(self, *args, **kwargs):
        countries = Country.objects.all()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.update_or_create_dispute_and_compliance, country) for country in countries]
            concurrent.futures.wait(futures)
