# 🤖 Cover Letter AI Agent

This project is an AI-powered agent that fully automates the cover letter creation process. You provide a job role and a company name, and the agent:

1.  **Generates** a unique, tailored cover letter using the Google Gemini API.
2.  **Accesses** your Google Drive to copy a "Cover Letter Template".
3.  **Edits** the new Google Doc to fill in the AI-generated text and company details.
4.  **Exports** the final, formatted document as a PDF to your local folder.

This agent is built using the **Google Agent Development Kit (ADK)**, which orchestrates the entire multi-step workflow.

---

## ✨ Features

* **AI-Powered Generation:** Uses the Google Gemini API to write compelling cover letters based on your personal profile.
* **Google Workspace Automation:** Integrates directly with the Google Drive and Google Docs APIs to create and edit documents.
* **Automatic PDF Export:** Saves the final, formatted cover letter directly to your project folder as a PDF.
* **Agentic Workflow:** Built with the Google ADK, which intelligently uses tools to complete its tasks (e.g., `copy_drive_template`, `update_google_doc`, `export_doc_as_pdf`).
* **Simple CLI:** Easy to run from your terminal with a single command.

---

## 🛠️ Tech Stack

* **Python** 3.11+
* **Google Agent Development Kit** (`google-adk`)
* **Google Gemini API** (`google-generativeai`)
* **Google Drive API** (`google-api-python-client`)
* **Google Docs API** (`google-api-python-client`, `google-auth-oauthlib`)

---

## 🚀 Setup & Installation

This project requires setting up credentials for both Google AI and Google Workspace.
