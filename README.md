# IT Access Guardian v3 - Full ADK Project
This project implements the "IT Access Guardian" using the Google Agent Development Kit (ADK) Python framework. It has been built to satisfy all core ADK concepts requested for the Kaggle 5-Day AI Agents Intensive Course Capstone.

Our project is submitted under the Enterprise Agents track.

## Team:
 - Ajay (Project Manager)
 - Prabhu (IT Admin)
 - Laxmi (Developer)
 - Anwesha (Developer)
   
## Pitch: "AccessBot: An autonomous, auditable AI agent that solves the IT helpdesk bottleneck. It autonomously enforces enterprise policy, manages resources, and provides complete observability, all built on the Google ADK."

##*Core Concepts Implemented*
We have implemented all 5 workflows (A-E) plus duplicate checking, using the following ADK key concepts:
 - [x] Tools (Custom): We built 5 custom Python tools with the @tool decorator (find_employee_by_email, find_policy_for_user, check_audit_log_for_duplicate, append_to_audit_log, send_gmail).
 - [x] Sessions & Memory: The AdkFastApiAdapter and UuidSessionIdSingleton are used to automatically manage conversational state. The agent remembers who the user is (e.g., sam.sales@company.demo) across multiple turns.
 - [x] Agent Evaluation: The run_evaluation.py script provides a full 7-case test suite. It uses tool_call to verify the agent's actions (e.g., "did it really log 'Rejected'?") and llm_as_judge to verify the agent's words (e.g., "did it correctly state the status?").
 - [x] Observability: AdkLogging.setup_logging() and AdkTrace.setup_trace() are implemented. This provides full visibility into the agent's decision-making (LLM prompts, tool selection, tool outputs) for debugging and tracing.
 - [x] Agent Deployment (A2A Protocol): The agent is deployed as a FastAPI web service, not a simple script. This makes it an A2A-compatible endpoint that any other service or agent can call via HTTP.
 - [x] Multi-agent system (Conceptual): Our agent is the first agent in a multi-agent system. It handles the user-facing task and then (via send_gmail) hands off the workflow to the next "agents" in the process: the Manager (for approval) and the IT Admin (for provisioning).

## How to Run This Project
You will need two terminals.
 - ## Terminal 1: Run the Agent Server
  1. Install Dependencies:
  - pip install "google-cloud-adk[fastapi,google,trace]" uvicorn httpx

  2. Set Google API Key:
  - The agent uses Gemini. You must set your API key in the environment.
  -(Replace YOUR_API_KEY_HERE with your actual key)
  - export GOOGLE_API_KEY="YOUR_API_KEY_HERE"

  3. Run the Server:
  - python it_guardian_agent.py

  - Keep this server running. You will see it print:
  - Access the API at http://127.0.0.1:8000/docs
  - 
 - ## Terminal 2: Run the Evaluation
 Once the server in Terminal 1 is running, you can run the evaluation script to test it.
 1. Set Google API Key:
 - This terminal also needs the API key for the "LLM as Judge" to work.
 - export GOOGLE_API_KEY="YOUR_API_KEY_HERE"

 2. Run the Evaluation Script:
 - python run_evaluation.py

 3. Analyze Results: You will see a summary in your terminal showing that all 7 tests passed or failed.

## How to Play Manually (Optional)
You can "talk" to your agent manually by using the FastAPI docs page.
Open your browser to http://127.0.0.1:8000/docs.
Find the /invoke endpoint and click "Try it out."
Start the conversation.
 - Turn 1: { "text": "Hi" }
 - Turn 2: { "text": "I am sam.sales@company.demo", "session_id": "PASTE_SESSION_ID_FROM_TURN_1" }
 - ...and so on.

## How to Deploy to GitHub (A Step-by-Step Guide)
Here is how to take your local project and publish it to a new GitHub repository.
 - Prerequisites
   - Git Installed: You must have Git installed on your computer.
   - GitHub Account: You must have a free GitHub account.
 - Step 1: Create the .gitignore (Critical for Security)
I have already created a .gitignore file for you. This file tells Git to ignore sensitive files, so they are never uploaded to GitHub.
This includes:
  - Your virtual environment (venv/)
  - Python cache files (__pycache__/)
  - Any file named .env (where you would store your API key)
 - Step 2: Initialize Your Local Git Repository
Run these commands from your project's root folder (the one containing all your files).
 - Initialize Git: This turns your folder into a Git repository.
   
   ```bash
   git init -b main


 - Add the .gitignore: This is the first file you should add and commit.

   ```bash
     git add .gitignore

Note: If you are using an existing repo, just add the new files.
git add run_evaluation.py README.md


 - Make Your Commit:

   ```bash
   git commit -m "Feat: Add in-depth tests for rejection and deprovisioning"


- Step 3: Create a New Repository on GitHub
(If you haven't already)
1. Go to GitHub.com and log in.
2. Click the + icon in the top-right corner and select "New repository".
3. Name your repository (e.g., it-guardian-agent-adk).
4. Make it Public (required for the competition).
5. Do NOT initialize it with a README or .gitignore (you already have those).
6. Click "Create repository".
   
- Step 4: Connect and Push Your Code
GitHub will show you a page with commands. You will use the "push an existing repository from the command line" commands.
1. Connect Your Local Repo to GitHub (if new):
Copy the URL from your new GitHub repo.
git remote add origin [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)

2. Push Your Code:
This sends your committed files (main branch) to GitHub (origin).
git push -u origin main


## WARNING: CRITICAL SECURITY INFORMATION
NEVER, EVER commit your GOOGLE_API_KEY to GitHub.
 - Your .gitignore file is set up to ignore .env files, which is the standard place to store API keys.
 - The way you are currently using the key (as an environment variable export GOOGLE_API_KEY="...") is correct and safe, as it is not part of your code.
 - DO NOT hard-code your key into it_guardian_agent.py like this:
   
# DO NOT DO THIS:
llm_provider = GoogleLlm(api_key="sk-...") 


If you accidentally commit a key, GitHub will find it, revoke it, and email you immediately. You should treat your API key like a password.
