import os
import openai
from dotenv import load_dotenv
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, PromptHelper, LangchainEmbedding, ServiceContext,PromptHelper
import openai
from langchain.embeddings import OpenAIEmbeddings
from llama_index.llm_predictor import LLMPredictor

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from llama_index import StorageContext, load_index_from_storage

load_dotenv()

class Qnabot:

    openai_api_key = os.getenv("openai_api_key")

    # def __init__(self):
               
    def load_wikipedia_documents(self,document_path):
         documents=SimpleDirectoryReader(document_path).load_data()
         return documents
    
    def create_gptindex(self,document_path):
        documents=self.load_wikipedia_documents(document_path)
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo",system_prompt="You are an expert on the articles given in Wikipedia and your job is to answer technical questions. Keep your answers technical and based on facts – do not hallucinate features.", max_tokens=512))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

        # service_context = ServiceContext.from_defaults(chunk_size_limit=3000)
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        # index.save_to_disk('artifacts/wikipedia_index.json')///
        index.storage_context.persist()
        return index
    
    def load_gptindex(self,document_path):
        try:
            # index = GPTVectorStoreIndex.load_from_disk('artifacts/wikipedia_index.json')///
            
            storage_context = StorageContext.from_defaults(persist_dir="./storage")
            # load index
            index = load_index_from_storage(storage_context)
        except FileNotFoundError:
            index = self.create_gptindex(document_path)
        return index
    
    def query_gptindex(self,gptindex):
        query_engine = gptindex.as_query_engine()
        while True:
            prompt = input("Query is :")
            response = query_engine.query(prompt)
            print(response)


    # def message_init(self):
    #     all_messages=[]
    #     all_messages = [{"role": "system", "content": """You’re a helpful assistant for a information retrieval system. You need to refer the
    #                   wikipedia related topics in the knowledge base and provide responses to the queries"""},
    #     {"role": "user", "content": ""} ] 
    #     return all_messages
                                    
    def generate_chat(self,document_path,user_input):
       
        # llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo",system_prompt="You are an expert on the articles given in Wikipedia and your job is to answer technical questions. Keep your answers technical and based on facts – do not hallucinate features.", max_tokens=512))
        # service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
        # documents = self.load_wikipedia_documents(document_path)
  
        # index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)#, prompt_helper=prompt_helper)
        # #query_engine = index.as_query_engine(service_context=service_context, verbose=True)
        index = self.load_gptindex(document_path)
        chat_engine = index.as_query_engine()
        all_messages=[]
        
        all_messages.append({"role": "human","content": user_input})
        response = chat_engine.query(user_input)
        print(response)
        all_messages.append({"role": "bot","content": response.response})
        return response,all_messages
    
    def first_chat(self,document_path):
        created_index = self.create_gptindex(document_path)
        return created_index

    


