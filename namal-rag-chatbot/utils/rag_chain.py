import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from utils.prompts import SYSTEM_PROMPT

load_dotenv()

def create_rag_response(query, retrieved_docs):

    context = "\n\n".join([
    doc.page_content[:1500] for doc in retrieved_docs
    ])

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant"
    )
    final_prompt = f"""
You are the Namal University AI Assistant.

RULES:
- Never claim to be a real person.
- Never pretend to be faculty or staff.
- Only say "I am the Namal University AI Assistant" if the user asks about your identity.
- Answer naturally and professionally.
- Use ONLY the provided context.
- Do not invent information.
- If information is unavailable, say:
  "This information is not currently available in the provided university dataset."

Context:
{context}

Question:
{query}

Answer:
"""
    response = llm.invoke(final_prompt)

    return response.content