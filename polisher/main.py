import os
from dotenv import load_dotenv

# Import your agents
from .refactor_agent import refactor_variable_names
from .comment_agent import add_file_comments
from .syntax_agent import fix_syntax_and_edges
from .summary_agent import generate_file_summary
from .security_agent import security_scan
from .readme_agent import update_readme
from .ignore_agent import manage_gitignore
from .git_agent import deploy_changes

load_dotenv()

def get_all_files(root_dir="."):
    """
    Recursively finds all source files, excluding hidden folders 
    and the pipeline's own files.
    """
    allowed_extensions = {'.py', '.js', '.html', '.css'}
    # Files to ignore (the pipeline itself and config)
    ignored_files = {
        "main.py", "refactor_agent.py", "comment_agent.py", 
        "syntax_agent.py", "summary_agent.py", "security_agent.py", 
        "readme_agent.py", "ignore_agent.py", "git_agent.py", 
        ".env", "README.md"
    }
    
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories like .git or .venv
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in allowed_extensions and file not in ignored_files:
                # Store the relative path (e.g., 'src/app.py')
                full_path = os.path.relpath(os.path.join(root, file), root_dir)
                file_list.append(full_path)
    
    return file_list

def run_orchestrator():
    project_root = "."
    project_context = {}
    tech_stack_detected = set()

    # 1. AUTO-DISCOVER FILES
    files_to_process = get_all_files(project_root)
    
    if not files_to_process:
        print("📭 No files found to process.")
        return

    print(f"🔎 Found {len(files_to_process)} files: {files_to_process}")

    # 2. PRE-SCAN (SECURITY)
    for path in files_to_process:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not security_scan(path, content):
            print(f"🛑 SECURITY HALT: {path}")
            return

    # 3. TRANSFORMATION LOOP
    for path in files_to_process:
        print(f"\n💎 Processing: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()

        data = refactor_variable_names(path, data)
        data = add_file_comments(path, data)
        data = fix_syntax_and_edges(path, data)

        # Summarize for the final README
        summary = generate_file_summary(path, data)
        project_context[path] = summary

        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
        
        tech_stack_detected.add(os.path.splitext(path)[1])

    # 4. HYGIENE & DOCS
    # manage_gitignore(project_root, list(tech_stack_detected))
    # update_readme(project_root, project_context)

    # 5. DEPLOY
    deploy_changes(project_root)
    print("\n✨ PIPELINE FINISHED SUCCESSFULLY.")

if __name__ == "__main__":
    run_orchestrator()