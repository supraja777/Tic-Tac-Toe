import re
import os
from git import Repo  # pip install GitPython
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def deploy_changes(repo_path: str):
    """
    Analyzes git diff, classifies the change, and generates a custom tagged commit message.
    """
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print("❌ Error: Not a git repository.")
        return

    repo = Repo(repo_path)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

    # 1. Get the 'diff'
    diff = repo.git.diff(None)
    if not diff:
        diff = repo.git.diff("--cached")

    if not diff:
        print("     ℹ️ No changes detected to commit.")
        return

    # 2. Ask AI to classify and write the message
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a git automation tool. Analyze the diff and choose the BEST tag:\n"
            "- [REFACTOR] for renaming variables, cleaning code, or changing structure without changing logic.\n"
            "- [UPDATE] for changing or improving existing business logic.\n"
            "- [ADD] for adding new features, files, or documentation.\n"
            "- [DELETE] for removing code or files.\n\n"
            "STRICT FORMATTING:\n"
            "1. Format: [TAG] <short description>\n"
            "2. Output ONLY the message text. No intro, no quotes, no backticks.\n"
            "3. Maximum 60 characters."
        )),
        ("user", "Write a commit message for this diff:\n\n{diff}")
    ])

    print("  -> Agent 8: Classifying changes and generating message...")
    
    chain = prompt | llm
    response = chain.invoke({"diff": diff[:5000]})
    
    # 3. Clean the output string
    commit_msg = response.content.strip()
    commit_msg = commit_msg.replace('`', '').replace('"', '').replace("'", "")
    commit_msg = commit_msg.split('\n')[0]

    # 4. Git Operations
    try:
        print(f"     📝 Final Commit Message: {commit_msg}")
        
        # Stage all changes
        repo.git.add(A=True)
        
        # Commit
        repo.index.commit(commit_msg)
        
        # Push to remote
        print("     ☁️ Pushing to remote...")
        origin = repo.remote(name='origin')
        origin.push()
        
        print("     🚀 Pushed to GitHub successfully!")
        
    except Exception as e:
        print(f"   ❌ Git operation failed: {e}")

if __name__ == "__main__":
    deploy_changes(".")