import os
from dotenv import load_dotenv

# Relative imports are correct for package structure
from .refactor_agent import refactor_variable_names
from .comment_agent import add_file_comments
from .syntax_agent import fix_syntax_and_edges
from .summary_agent import generate_file_summary
from .security_agent import security_scan
from .readme_agent import update_readme
from .ignore_agent import manage_gitignore
from .git_agent import deploy_changes

# Force load .env from the directory where the user is running the command
load_dotenv(os.path.join(os.getcwd(), '.env'))

def get_all_files(root_dir):
    allowed_extensions = {'.py', '.js', '.html', '.css'}
    # Robust check: ignore anything that looks like an agent or the main script
    
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            
            # Filter logic: ignore the tool's own files even if they are in the folder
            if ext in allowed_extensions:
                if "agent" in file or file == "main.py" or file == "setup.py":
                    continue
                
                full_path = os.path.relpath(os.path.join(root, file), root_dir)
                file_list.append(full_path)
    
    return file_list

def run_orchestrator():
    # IMPORTANT: Target the folder where the user typed 'polish'
    project_root = os.getcwd() 
    project_context = {}
    tech_stack_detected = set()

    print(f"🚀 AI Polisher active in: {project_root}")

    # 1. AUTO-DISCOVER FILES
    files_to_process = get_all_files(project_root)
    
    if not files_to_process:
        print("📭 No files found to process in this directory.")
        return

    print(f"🔎 Found {len(files_to_process)} files: {files_to_process}")

    # 2. PRE-SCAN (SECURITY)
    for path in files_to_process:
        abs_path = os.path.join(project_root, path)
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not security_scan(path, content):
            print(f"🛑 SECURITY HALT: {path} contains sensitive data.")
            return

    # 3. TRANSFORMATION LOOP
    for path in files_to_process:
        abs_path = os.path.join(project_root, path)
        print(f"\n💎 Polishing: {path}")
        
        with open(abs_path, 'r', encoding='utf-8') as f:
            data = f.read()

        # Agents process the code
        data = refactor_variable_names(path, data)
        data = add_file_comments(path, data)
        data = fix_syntax_and_edges(path, data)

        summary = generate_file_summary(path, data)
        project_context[path] = summary

        # Save changes
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(data)
        
        tech_stack_detected.add(os.path.splitext(path)[1])

    # 4. HYGIENE & DOCS (Uncomment these when ready!)
    manage_gitignore(project_root, list(tech_stack_detected))
    update_readme(project_root, project_context)

    # 5. DEPLOY
    deploy_changes(project_root)
    print("\n✨ PIPELINE FINISHED SUCCESSFULLY.")

if __name__ == "__main__":
    run_orchestrator()