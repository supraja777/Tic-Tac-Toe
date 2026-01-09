from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

class FileSummary(BaseModel):
    summary: str = Field(description="A 2-sentence summary of the file's purpose and main functions.")

def generate_file_summary(file_path: str, code: str) -> str:
    """
    Analyzes the code and returns a brief summary for the README.
    """
    print(f"  -> Agent 4: Summarizing {file_path}...")
    
    structured_llm = llm.with_structured_output(FileSummary)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Technical Architect. Look at the provided code and provide a "
            "concise, professional 2-sentence summary of what this file does within the project."
        )),
        ("user", "Summarize this file ({file_path}):\n\n{code}")
    ])

    chain = prompt | structured_llm

    try:
        result = chain.invoke({"file_path": file_path, "code": code})
        return result.summary
    except Exception as e:
        print(f"   ❌ Summary failed for {file_path}: {e}")
        return "No summary available."