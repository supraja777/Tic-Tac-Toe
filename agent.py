from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# LLM CONFIG — CONTENT EXTRACTION ONLY
# ==================================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)


