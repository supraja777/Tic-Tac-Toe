from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

class SecurityAudit(BaseModel):
    is_safe: bool = Field(description="True if no sensitive data is found.")
    found_secrets: list[str] = Field(description="List of sensitive items found (e.g., 'OpenAI Key', 'DB Password').")
    recommendation: str = Field(description="Instructions on how to fix the leak.")

def security_scan(file_path: str, code: str) -> bool:
    print(f"  -> Agent 6: Security scan for {file_path}...")
    structured_llm = llm.with_structured_output(SecurityAudit)
    
    prompt = f"Analyze the following code for hardcoded secrets (API keys, passwords, tokens):\n\n{code}"
    result = structured_llm.invoke(prompt)

    if not result.is_safe:
        print(f"  ❌ SECURITY ALERT in {file_path}: Found {result.found_secrets}")
        print(f"  💡 Suggestion: {result.recommendation}")
        return False
    return True