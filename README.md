# 🛡️ AI Code Polisher

**AI Code Polisher** is a professional-grade, multi-agent automation system that cleans, refactors, documents, secures, and deploys your codebase — all with a single command.

Built on **Groq** and **Llama 3**, it removes the repetitive, error-prone parts of software maintenance so you can focus on building features, not fixing formatting or chasing secrets.

---

## ✨ Why AI Code Polisher?

Modern projects grow fast—and so does technical debt.  
AI Code Polisher acts like an **AI-powered senior engineer**, reviewing your entire repository end-to-end and applying best practices automatically.

**One command → production-ready codebase.**

---

## 🚀 Core Features

This system is powered by **8 specialized AI agents**, each responsible for a critical development task:

### 🔍 Auto-Discovery Agent
- Recursively scans your project
- Safely detects `.py`, `.js`, `.html`, and `.css` files
- Ignores system and protected directories

### 🛡️ Security Guard Agent
- Detects hardcoded API keys, tokens, and secrets
- Blocks unsafe files from being processed
- Prevents accidental credential leaks

### 💎 Refactor Architect Agent
- Renames variables and functions intelligently
- Improves readability and semantic clarity
- Enforces clean, professional naming conventions

### ✍️ Documentation Writer Agent
- Adds consistent file headers
- Generates docstrings and block comments
- Improves long-term maintainability

### 🛠️ Syntax Linter Agent
- Fixes indentation and formatting issues
- Cleans brackets, spacing, and minor syntax errors
- Keeps code style consistent across the project

### 📝 Summary Analyst Agent
- Produces high-level summaries for every file
- Generates structured documentation insights
- Feeds content into README generation

### 🧹 Hygiene Manager Agent
- Automatically updates `.gitignore`
- Detects frameworks and tools in use
- Prevents unnecessary or sensitive files from being committed

### 📦 Git Courier Agent
- Stages all changes automatically
- Commits with meaningful tags (e.g. `[REFACTOR]`, `[DOCS]`)
- Pushes to your active Git branch

---

## 📦 Installation

Install directly from GitHub using `pip`:

```bash
pip install git+https://github.com/supraja777/Tic-Tac-Toe.git
```

---

## ⚙️ Setup (Required)

To keep your credentials secure, the API key is **not bundled** with the package.

### 1️⃣ Get a Groq API Key

https://console.groq.com

### 2️⃣ Create a `.env` file

In the root of the project you want to polish:

```env
GROQ_API_KEY=your_gsk_key_here
```

🔐 **Security Reminder:**  
Ensure `.env` is added to `.gitignore`.

---

## 🛠️ Usage

Navigate to any project directory and run:

```bash
polish
```

### What happens next?

1. Scanning – Detects all eligible files  
2. Validation – Confirms API key and security status  
3. Transformation – Runs each AI agent sequentially  
4. Deployment – Commits and pushes changes to Git  

---

## 🏗️ Project Architecture

```plaintext
polisher/
├── __init__.py
├── main.py              # Agent orchestrator
├── refactor_agent.py    # Variable & function renaming
├── comment_agent.py     # Docstrings & file headers
├── syntax_agent.py      # Formatting & linting
├── summary_agent.py     # File-level summaries
├── security_agent.py    # Secret detection
├── readme_agent.py      # README generation
├── ignore_agent.py      # .gitignore management
└── git_agent.py         # Git automation
```

---

## ⚠️ Important Notes

- **Free Tier Limits:** Very large files (>10k characters) may hit Groq TPM limits.
- **Recommended:** Run on a separate Git branch to review AI changes before merging.
- **Overwrite Warning:** Files are rewritten in place. Git is your safety net.

---

