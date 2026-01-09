import os
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

class ReadmeOutput(BaseModel):
    content: str = Field(description="The full content for the README.md file in Markdown format.")
    detected_tech_stack: list[str] = Field(description="List of technologies detected (e.g., Python, HTML, FastAPI).")

def update_readme(project_root: str, file_summaries: dict) -> str:
    """
    Step 5: Creates or updates the README.md based on the entire project context.
    'file_summaries' is a dictionary: { "filename.py": "Description of what it does" }
    """
    print(f"  -> Agent 5: Generating/Updating README.md...")
    
    structured_llm = llm.with_structured_output(ReadmeOutput)
    
    # Format the summaries for the prompt
    context_str = "\n".join([f"- {name}: {desc}" for name, desc in file_summaries.items()])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Technical Documentation Expert. Your goal is to write a professional README.md.\n\n"
            "THE README SHOULD INCLUDE:\n"
            "1. Project Title (derived from folder name or files).\n"
            "2. Project Overview (brief description).\n"
            "3. Technology Stack (list of languages/frameworks detected).\n"
            "4. File Structure (explain what each main file does based on provided summaries).\n"
            "5. How to Run/Install (best guess based on file types).\n\n"
            "Use clean Markdown formatting with tables and lists."
        )),
        ("user", f"Project Path: {project_root}\n\nFile Summaries:\n{context_str}")
    ])

    chain = prompt | structured_llm

    try:
        result = chain.invoke({"project_root": project_root})
        
        readme_path = os.path.join(project_root, "README.md")
        
        # Write the file
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(result.content)
            
        print(f"     ✅ README.md created/updated successfully.")
        print(f"     🛠️ Tech Stack Detected: {', '.join(result.detected_tech_stack)}")
        
        return result.content
    except Exception as e:
        print(f"   ❌ README Agent failed: {e}")
        return ""