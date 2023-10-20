
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.document_loaders import TextLoader
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from dotenv import load_dotenv
from util.templates import Template
from util.firebase import FirebaseManager
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage


import os
import json
import datetime

load_dotenv()


class Agent:
    def __init__(self, payload):

        self.firebase = FirebaseManager()
        self.template = Template()
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        self.init_configuration(payload['filename']) if payload['filename'] != '' \
            else ''

    def init_configuration(self, filename):
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        self.absPath = os.path.abspath(os.path.join(current_script_dir, ".."))

        self.firebase.get_file_content_from_storage(filename)

        self.conversation_template = """{}"""

        dataset = self.load_dataset()
        docs = self.create_embedding(dataset)

        self.knowledge_base = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=docs.as_retriever())

    def load_dataset(self):
        loader = TextLoader(f"{self.absPath}\\dataset\\.txt", encoding='utf-8')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        dataset = text_splitter.split_documents(documents)
        return dataset

    def create_embedding(self, dataset):
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(
            dataset, embeddings, collection_name="state-of-union")
        return docsearch

    def ask(self, payload):
        conversation = []
        memory = ConversationBufferMemory(return_messages=True)
        resp = self.firebase.get_messages(
            payload['virtual_number'], payload['user_number'])
        if resp != None and type(resp) == list:
            for message in resp:
                memory.chat_memory.add_user_message(
                    message['content']) if message['role'] == 'Human' else memory.chat_memory.add_ai_message(message['content'])
                conversation.append(
                    f"{'Customer: ' if message['role']=='Human' else 'AI Agent: ' } {message['content']}")

        if payload['filename'] != '':

            prompt = self.template.base_template_simple().format(
                "\n".join(conversation), payload['query'])

            response = self.knowledge_base.run(prompt)
            conversation.append(f"AI Agent: {response}")
            memory.chat_memory.add_ai_message(response)

            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=self.template.SystemPrompt()),
                HumanMessagePromptTemplate.from_template(
                    "{human_input}"),
            ])

            chat_llm_chain = LLMChain(
                llm=self.llm,
                prompt=prompt,
                verbose=False,
            )

            chain_response = json.loads(chat_llm_chain.predict(
                human_input=self.conversation_template.format(
                    "\n".join(conversation))))

            if chain_response['status'] == 'incorrect':
                conversation.pop()
                conversation.append(f"AI Agent: {chain_response['correct']}")
                data = {
                    'virtual_number': payload['virtual_number'],
                    'user_number': payload['user_number'],
                    'message': {
                        'content': chain_response['correct'],
                        'role': 'AI',
                        'time': datetime.datetime.now()
                    },
                }
                status = self.firebase.add_message(data)
                return chain_response['correct'] if status else None

            elif chain_response['status'] == 'correct':
                data = {
                    'virtual_number': payload['virtual_number'],
                    'user_number': payload['user_number'],
                    'message': {
                        'content': response,
                        'role': 'AI',
                        'time': datetime.datetime.now()
                    },
                }
                status = self.firebase.add_message(data)
                return response if status else None

        else:
            prompt = PromptTemplate(
                input_variables=["history", "input"], template=self.template.base_template())
            conversation = ConversationChain(
                prompt=prompt,
                llm=self.llm,
                verbose=False,
                memory=memory
            )
            response = conversation.predict(input=payload['query'])
            data = {
                'virtual_number': payload['virtual_number'],
                'user_number': payload['user_number'],
                'message': {
                    'content': response,
                    'role': 'AI',
                    'time': datetime.datetime.now()
                },
            }
            status = self.firebase.add_message(data)
            return data if status else None
