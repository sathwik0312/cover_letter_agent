# agent.py
from google.adk.agents import Agent
from google.adk.models import Gemini
import cover_letter_agent.tools as tools  # <-- Import your new tools file

try:
    with open("profile.txt", "r") as f:
        MY_PROFILE = f.read()
    print("✅ Profile loaded successfully.")
except FileNotFoundError:
    print("❌ ERROR: 'my_profile.txt' not found.")
    print("Please create 'my_profile.txt' in the same directory.")
    MY_PROFILE = "ERROR: PROFILE NOT FOUND. PLEASE CREATE my_profile.txt"
except Exception as e:
    print(f"❌ ERROR: Could not read 'my_profile.txt': {e}")
    MY_PROFILE = "ERROR: PROFILE NOT FOUND."

# --- Your Template ID ---
TEMPLATE_ID = "https://docs.google.com/document/d/1efTTgaz9Lck95iVtZzSfpi6KhidWzg3c_lk1z6zA73I/edit?tab=t.0"

# --- The Agent Definition ---
cover_letter_agent = Agent(
    model="gemini-2.5-flash",
    name="cover_letter_agent",
    # Give the agent its tools
    tools=[
        tools.copy_drive_template,
        tools.update_google_doc,
        tools.export_doc_as_pdf,
    ],
    description="Your are an agent who creates a cover letter for a given company and role",
    # The instructions tell the LLM how to chain the tools
    instruction=f"""
    You are a cover letter writing assistant. Your goal is to generate a cover letter
    and save it as a PDF, it must contain only single page.
    
    Here is my personal profile for context:
    {MY_PROFILE}

    When the user gives you a role and a company, you must follow these steps in order:
    
    1.  **Generate Content:** First, you must generate the complete body text (2-3 paragraphs)
        for the cover letter. 
        - This text should be tailored to the role and company,using my profile.
        - **IMPORTANT: Do not create any "Dear Hiring Team,","sincerely, Sathwik" as they are already present in the template.
        - **IMPORTANT: Separate paragraphs with only a single newline
          character ('\n'), not double newlines ('\n\n'), to ensure correct spacing.**
        
    
    2.  **Copy Template:** Call the `copy_drive_template` tool.
        - Use "{TEMPLATE_ID}" for the `template_id`.
        - Create a `new_title` like "[Company] - [Role] - Cover Letter".
        - You MUST wait for this tool to return the `new_doc_id`.
        
    3.  **Update Document:** Call the `update_google_doc` tool.
        - Use the `new_doc_id` from step 2.
        - Pass the user's `company` and `role`.
        - Pass the `generated_body` text from step 1.
    
    4.  **Export PDF:** Call the `export_doc_as_pdf` tool.
        - Use the `new_doc_id` from step 2.
        - Create a `pdf_filename` like "[Company]_Cover_Letter.pdf".
        
    5.  **Confirm:** Once all steps are complete, respond to the user with a final
        confirmation message, including the PDF filename.
    """
)