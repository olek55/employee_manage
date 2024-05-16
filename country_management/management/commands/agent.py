from django.core.management.base import BaseCommand
from country_management.models import Leave, Country
from openai import OpenAI
import concurrent.futures
import json
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain_community.tools.tavily_search import TavilySearchResults



import getpass
import os



class Command(BaseCommand):
    help = 'Let an agent search the web'

    def handle(self, *args, **options):
        os.environ["TAVILY_API_KEY"] = getpass.getpass()
        tool = TavilySearchResults()
        
        result = tool.invoke({"query": "What is the minimum wage in Germany?"})
        print(result)