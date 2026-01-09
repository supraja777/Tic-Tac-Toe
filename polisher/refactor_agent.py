import os
from typing import List
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# LLM CONFIG
# ==================================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0  # Keeping it at 0 for strict logic preservation
)

# 1. Define the Structured Output Schema
class FileRefactor(BaseModel):
    """Schema for the refactored code output."""
    file_path: str = Field(description="The path to the file being refactored")
    refactored_code: str = Field(description="The full code with improved variable names only")
    changes_made: List[str] = Field(description="A list of specific variable names that were renamed")

# 2. Pipeline-Ready Function
def refactor_variable_names(file_path: str, current_data: str) -> str:
    """
    Step 1 of the pipeline: Refactors variable names.
    Takes code string -> Returns improved code string.
    """
    print(f"  -> Agent 1: Refactoring variables in {file_path}...")
    
    # Bind structured output to handle JSON/Backslash issues automatically
    structured_llm = llm.with_structured_output(FileRefactor)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a 'Clean Code' specialist. Your ONLY mission is to improve variable naming, "
            "readability, and indentation.\n\n"
            "STRICT RULES:\n"
            "1. DO NOT change the logic, algorithms, or functionality.\n"
            "2. DO NOT add new features or delete existing code.\n"
            "3. Use descriptive, industry-standard naming (e.g., 'user_id' instead of 'uid').\n"
            "4. Maintain the exact same file format.\n"
            "5. Ensure all code escape characters (like \\n, \\t) are handled correctly."
        )),
        ("user", "Refactor the following code from file {file_path}:\n\n{code}")
    ])

    chain = prompt | structured_llm

    try:
        # Run the agent
        result = chain.invoke({
            "file_path": file_path, 
            "code": current_data
        })
        
        # Log changes to console for tracking
        if result.changes_made:
            print(f"     ✅ Renamed: {', '.join(result.changes_made)}")
        
        # Return only the refactored code string for the next agent in the pipeline
        return result.refactored_code

    except Exception as e:
        print(f"   ❌ Refactoring failed: {e}")
        # Return the original data so the pipeline doesn't break
        return current_data

# ==================================================
# TEST BLOCK (Optional)
# ==================================================
if __name__ == "__main__":
    test_code = "def f(a, b): return a + b"
    improved = refactor_variable_names("test.py", test_code)
    print(f"\nFinal Result:\n{improved}")