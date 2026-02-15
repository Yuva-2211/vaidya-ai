import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from groq import Groq

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


pc = Pinecone(api_key=PINECONE_API_KEY)

vectorstore = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


groq_client = Groq(api_key=GROQ_API_KEY)

def ask_rag(question: str):

    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a strictly evidence-grounded Ayurvedic knowledge assistant.

INSTRUCTIONS:
1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. If the answer is not clearly found in the context, respond exactly with:
   "Information not available in the provided sources."
4. Do NOT guess, assume, or infer beyond what is explicitly stated.
5. If multiple remedies are mentioned, list them separately.
6. Provide clear step-by-step preparation instructions if available.
7. Mention ingredients, quantities, and duration only if present in context.
8. If the context includes source titles or metadata, reference them briefly.
9. Don't Use any ** or emoji in the output , and proper line breaks
10. Give decent Spacing for the answer , keep it structured 
11. Dont give answer without proper knowledge

OUTPUT FORMAT:

Remedy Name:
Brief Description (1-2 lines from context)

Ingredients:
- List exactly as mentioned

Preparation:
1. Step-by-step process

Dosage / Usage:
- As stated in source

Source:
- Mention book name or metadata if available

Safety Note:
- Include a short general disclaimer:
  "This information is for educational purposes only. Consult a qualified healthcare professional before use."

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = groq_client.chat.completions.create(
       model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content




print("Rag is initiated!!")