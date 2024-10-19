from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import SystemMessage, HumanMessage
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
embed_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=os.getenv("OPENAI_API_KEY"))
COLLECTION_NAME = "retail-fundamentals"
CHROMA_LOCATION = "./.vector-index"
chroma_client = chromadb.PersistentClient(path=CHROMA_LOCATION)

def ingest_data():

    if collection_exists():
        return

    print(f"Loading vector index into collection {COLLECTION_NAME}. This might take a little while....")
    create_collection()
    loader = PyPDFLoader("./docs/fundamentals.pdf")
    document = loader.load()

    docs = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 20,        
    ).split_documents(document)

    Chroma.from_documents(
        documents=docs, 
        embedding=embed_model, 
        persist_directory=CHROMA_LOCATION,
        collection_name=COLLECTION_NAME
    )

def retrieve(query: str):
    index = Chroma(collection_name=COLLECTION_NAME, embedding_function=embed_model, client=chroma_client)
    context = [i.page_content + "\n" for i in index.similarity_search(query=query, k=5)]

    messages = [
        SystemMessage(content=f"""
            You are an expert at retails fundamentals and best practices. Please help answer user questions using the content supplied below.                      
            Content:
            {context}
        """),
        HumanMessage(content=query)
    ]

    return llm.invoke(messages).content


def create_collection():
    return chroma_client.create_collection(COLLECTION_NAME)

def collection_exists():
    existing_collections = chroma_client.list_collections()    
    return any(collection.name == COLLECTION_NAME for collection in existing_collections)

def delete_collection():
    if collection_exists():
        chroma_client.delete_collection(COLLECTION_NAME)
