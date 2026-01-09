import os
from typing import List
from dotenv import load_dotenv

# Import your specialized functions from your other files
# (Ensure these files exist in the same directory)
from refactor_agent import refactor_variable_names
from comment_agent import add_file_comments
from syntax_agent import fix_syntax_and_edges

from summary_agent import generate_file_summary
from readme_agent import update_readme

load_dotenv()

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# LLM CONFIG — USING STRUCTURED OUTPUT
# ==================================================
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0  # Set to 0 for consistent code refactoring
)

def run_code_improvement_pipeline(file_paths: List[str]):
    """
    Orchestrates the multi-step transformation of code files.
    Logic: Read -> Step 1 -> Step 2 -> Step 3 -> Final Write
    """
    project_context = {}
    for path in file_paths:
        if not os.path.exists(path):
            print(f"⚠️ File not found, skipping: {path}")
            continue

        print(f"\n--- 🚀 Starting Pipeline for: {path} ---")

        # 1. READ ORIGINAL CONTENT
        try:
            with open(path, 'r', encoding='utf-8') as f:
                current_data = f.read()
        except Exception as e:
            print(f"❌ Error reading file {path}: {e}")
            continue

        try:
            # 2. STEP ONE: REFACTOR VARIABLE NAMES
            # We pass the result of one function into the next
            print("Running Step 1: Variable Refactoring...")
            current_data = refactor_variable_names(path, current_data)

            # 3. STEP TWO: ADD FILE COMMENTS
            print("Running Step 2: Adding File Headers...")
            current_data = add_file_comments(path, current_data)

            # 4. STEP THREE: (Add your syntax/edge case function here when ready)
            print("Running Step 3: Syntax & Edge Case Fixes...")
            current_data = fix_syntax_and_edges(path, current_data)

            file_summary = generate_file_summary(path, current_data)
            project_context[path] = file_summary

            # 6. FINAL WRITE
            # This only happens if all previous steps completed without crashing
            with open(path, 'w', encoding='utf-8') as f:
                f.write(current_data)

            print(f"✅ Pipeline Successfully Completed for: {path}")

        except Exception as e:
            # If any step fails, the 'with open(w)' is never reached, protecting your file
            print(f"❌ Pipeline aborted for {path} due to error: {e}")
            
    print("\n📚 FINAL STEP: Generating Project README...")
    update_readme(".", project_context)
    print("✨ ALL TASKS COMPLETE.")

if __name__ == "__main__":
    # Define the files you want to run through the 'car wash'
    target_files = [
        "index.html",
        "style.css",
        "script.js",
        "app.py"
    ]
    
    run_code_improvement_pipeline(target_files)