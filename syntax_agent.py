import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# 1. Structured Output to ensure the agent reports its tiny fixes
class SafeSyntaxFix(BaseModel):
    fixed_code: str = Field(description="The code with only minor, safe syntax corrections applied.")
    fix_log: list[str] = Field(description="List of tiny fixes made (e.g., 'fixed typo in import', 'closed div tag')")

def fix_syntax_and_edges(file_path: str, current_data: str) -> str:
    """
    Step 3 of the pipeline: Minor syntax cleanup.
    Strictly focuses on small errors that prevent crashes without touching logic.
    """
    print(f"  -> Agent 3: Running minor syntax check on {file_path}...")
    
    ext = os.path.splitext(file_path)[1].lower()
    structured_llm = llm.with_structured_output(SafeSyntaxFix)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            f"You are a cautious 'Safe-Fix' Linter for {ext} files. Your goal is to fix only trivial errors.\n\n"
            "ALLOWED FIXES:\n"
            "1. Fix obvious typos in standard library imports or keywords.\n"
            "2. Close unclosed brackets (), [], {} or HTML tags.\n"
            "3. Fix inconsistent indentation that might cause errors.\n"
            "4. Add basic null-checks if a variable is obviously used without one.\n\n"
            "STRICT PROHIBITIONS:\n"
            "- DO NOT change any business logic or algorithms.\n"
            "- DO NOT remove any comments added in previous steps.\n"
            "- If the code is already syntactically correct, return it EXACTLY as it is.\n"
            "- DO NOT add new features."
        )),
        ("user", "Perform a safe syntax check on this code from {file_path}. Return the full code:\n\n{code}")
    ])

    chain = prompt | structured_llm

    try:
        result = chain.invoke({"file_path": file_path, "code": current_data})
        
        # Log the minor fixes to the console
        if result.fix_log:
            for fix in result.fix_log:
                print(f"     🔧 Minor Fix: {fix}")
        else:
            print("     ✅ No syntax errors found.")
        
        # Length Guardrail: Ensure it didn't accidentally delete large chunks
        if len(result.fixed_code) < (len(current_data) * 0.95):
            print("   ⚠️ Fixer removed too much code. Reverting to previous state.")
            return current_data

        return result.fixed_code
        
    except Exception as e:
        print(f"   ❌ Syntax Agent encountered an error: {e}")
        return current_data