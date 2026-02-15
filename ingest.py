import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv


load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")


loader1 = PyPDFLoader("data/Ayurvedic-Home-Remedies-English.pdf")
loader2 = PyPDFLoader("data/The-Complete-Book-of-Ayurvedic-Home-Remedies.pdf")

docs1 = loader1.load()
docs2 = loader2.load()

documents = docs1 + docs2

print(f"This is the length of the first book{len(docs1)}")
print(f"This is the length of the second  book{len(docs2)}")
print(f"This is the length of the final data {len(documents)}")



for doc in docs1:
    doc.metadata["source"] = "Ayurvedic-Home-Remedies-English"

for doc in docs2:
    doc.metadata["source"] = "The-Complete-Book-of-Ayurvedic-Home-Remedie"




splitter = RecursiveCharacterTextSplitter(
    chunk_size = 900,
    chunk_overlap = 200
)

chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )


vectorstore = PineconeVectorStore.from_documents(
    chunks,
    embeddings,
    index_name=INDEX_NAME
)





print("Data Ingestion Over ")