import os
from langchain_groq import ChatGroq

def manage_gitignore(project_root: str, tech_stack: list):
    """
    Creates or updates .gitignore based on the detected tech stack.
    """
    print(f"  -> Agent 7: Managing .gitignore...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    path = os.path.join(project_root, ".gitignore")
    existing_content = ""
    if os.path.exists(path):
        with open(path, "r") as f: existing_content = f.read()

    prompt = (
        f"Based on this tech stack: {tech_stack}, generate a standard .gitignore file. "
        f"Existing content:\n{existing_content}\n"
        "Return ONLY the plain text content for the file."
    )
    
    response = llm.invoke(prompt)
    
    with open(path, "w") as f:
        f.write(response.content)
    print("     ✅ .gitignore is up to date.")