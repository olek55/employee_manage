from django.core.management.base import BaseCommand
from country_management.models import Country, Payment
from openai import OpenAI
import concurrent.futures
import json
from dotenv import load_dotenv

import os


class Command(BaseCommand):
    help = 'Use chat gpt + web search to generate text'


    def handle(self, *args, **kwargs):
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
        from langchain.callbacks.base import BaseCallbackHandler
        from langchain.chains import RetrievalQAWithSourcesChain
        from langchain.retrievers.web_research import WebResearchRetriever
        from langchain_community.chat_models import ChatOpenAI
        from langchain_community.utilities import GoogleSearchAPIWrapper
        from langchain_community.vectorstores import FAISS
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.docstore import InMemoryDocstore

        def settings():
            # Vectorstore
            import faiss
            embeddings_model = OpenAIEmbeddings()
            embedding_size = 1536
            index = faiss.IndexFlatL2(embedding_size)
            vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

            # LLM
            llm = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0)

            # Search
            search = GoogleSearchAPIWrapper()

            # Initialize
            web_retriever = WebResearchRetriever.from_llm(
                vectorstore=vectorstore, llm=llm, search=search, num_search_results=3
            )

            return web_retriever, llm

        # Retrieve the question from the user
        question = input("Ask a question: ")

        if question:
            import logging

            logging.basicConfig()
            logging.getLogger("langchain.retrievers.web_research").setLevel(logging.INFO)

            # Load retriever and LLM objects
            retriever, llm = settings()

            # Generate answer with web search
            qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=retriever)
            result = qa_chain(question)
            # Print the answer and sources
            print('Answer:\n', result['answer'])