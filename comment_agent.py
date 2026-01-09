import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

class FileCommentary(BaseModel):
    full_code_with_comments: str = Field(description="The ENTIRE original code with comments inserted at the top and near functions.")

def add_file_comments(file_path: str, current_data: str) -> str:
    print(f"  -> Agent 2: Inserting Block-Style comments into {file_path}...")
    
    # Identify the extension to give the AI a hint
    ext = os.path.splitext(file_path)[1].lower()
    
    # Map extensions to specific instructions
    syntax_map = {
        ".py": "Python syntax (# for comments)",
        ".js": "JavaScript syntax (// for single lines, /* */ for blocks)",
        ".html": "HTML syntax (for comments)",
        ".css": "CSS syntax (/* */ for comments)"
    }
    
    target_syntax = syntax_map.get(ext, "the standard comment syntax for this file type")
    
    structured_llm = llm.with_structured_output(FileCommentary)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            f"You are a Senior Developer. Your task is to TAKE THE EXISTING CODE and INSERT structural comments using {target_syntax}.\n\n"
            "CRITICAL RULES:\n"
            "1. DO NOT DELETE ANY CODE. Your output must contain every single line of the original code.\n"
            "2. INSERT a major block header at the top (e.g., # ================== or ).\n"
            "3. INSERT numbered section headers (e.g., 1. Imports, 2. Logic).\n"
            "4. INSERT a one-line comment above every major function, tag block, or class.\n"
            "5. Maintain all existing logic and structure exactly as is."
        )),
        ("user", "Here is the code for {file_path}. Return the full code with your comments added:\n\n{code}")
    ])

    chain = prompt | structured_llm

    try:
        result = chain.invoke({"file_path": file_path, "code": current_data})
        
        # Verify the AI didn't just return an empty string or snippet
        if len(result.full_code_with_comments) < (len(current_data) * 0.7):
            print("   ⚠️ AI returned truncated code. Using original instead.")
            return current_data
            
        return result.full_code_with_comments
    except Exception as e:
        print(f"   ❌ Commenting failed: {e}")
        return current_data