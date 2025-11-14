# tools.py
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import io
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents"
]

def get_google_creds():
    """Gets valid Google API credentials.
    
    Handles the entire OAuth 2.0 flow:
    1. Looks for a valid 'token.json'.
    2. If expired, refreshes it.
    3. If not found, runs the login flow using 'credentials.json'.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                print("Refreshing expired credentials...")
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None # Force re-login
        
        # If no valid token, run the OAuth flow
        if not creds:
            try:
                print("Running Google login flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                print("FATAL ERROR: 'credentials.json' not found.")
                print("Please download it from Google Cloud Console and place it in this folder.")
                return None
            except Exception as e:
                print(f"Error during authentication flow: {e}")
                return None

        # Save the credentials for the next run
        try:
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            print("Credentials saved to token.json")
        except Exception as e:
            print(f"Error saving token.json: {e}")
    
    return creds

# --- YOUR CUSTOM TOOLS ---

def copy_drive_template(template_id: str, new_title: str) -> str:
    """
    Copies a Google Drive template file and returns the new file's ID.
    
    Args:
        template_id (str): The ID of the Google Doc template to copy.
        new_title (str): The name for the new document.
    """
    creds = get_google_creds()
    if not creds:
        return "Error: Could not get Google credentials."
        
    try:
        drive_service = build("drive", "v3", credentials=creds)
        new_doc = drive_service.files().copy(
            fileId=template_id,
            body={"name": new_title}
        ).execute()
        new_id = new_doc.get("id")
        print(f"Tool 'copy_drive_template' SUCCESS: New Doc ID is {new_id}")
        return new_id
    except HttpError as error:
        print(f"Tool 'copy_drive_template' ERROR: {error}")
        return f"Error copying file: {error}"
    except Exception as e:
        print(f"Tool 'copy_drive_template' UNEXPECTED ERROR: {e}")
        return f"An unexpected error occurred: {e}"


def update_google_doc(document_id: str, company: str, role: str, generated_body: str) -> str:
    """
    Replaces all placeholder text in a specific Google Doc.
    
    Args:
        document_id (str): The ID of the Google Doc to edit.
        company (str): The company name to insert.
        role (str): The role name to insert.
        generated_body (str): The AI-generated text for the letter body.
    """
    creds = get_google_creds()
    if not creds:
        return "Error: Could not get Google credentials."

    try:
        docs_service = build("docs", "v1", credentials=creds)
        
        requests = [
            {"replaceAllText": {"containsText": {"text": "{{COMPANY_NAME}}", "matchCase": True}, "replaceText": company}},
            {"replaceAllText": {"containsText": {"text": "{{ROLE_NAME}}", "matchCase": True}, "replaceText": role}},
            {"replaceAllText": {"containsText": {"text": "{{GENERATED_BODY}}", "matchCase": True}, "replaceText": generated_body}},
            # You can add more here, like {{DATE}}
        ]
        
        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={"requests": requests}
        ).execute()
        print(f"Tool 'update_google_doc' SUCCESS for Doc ID {document_id}")
        return f"Document {document_id} updated successfully."
    except HttpError as error:
        print(f"Tool 'update_google_doc' ERROR: {error}")
        return f"Error updating doc: {error}"
    except Exception as e:
        print(f"Tool 'update_google_doc' UNEXPECTED ERROR: {e}")
        return f"An unexpected error occurred: {e}"


def export_doc_as_pdf(document_id: str, pdf_filename: str) -> str:
    """
    Exports a Google Doc to a local PDF file.
    
    Args:
        document_id (str): The ID of the Google Doc to export.
        pdf_filename (str): The local filename to save the PDF as (e.g., "Google_Cover_Letter.pdf").
    """
    creds = get_google_creds()
    if not creds:
        return "Error: Could not get Google credentials."

    try:
        drive_service = build("drive", "v3", credentials=creds)
        
        request = drive_service.files().export_media(fileId=document_id, mimeType="application/pdf")
        
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"PDF Download progress: {int(status.progress() * 100)}%")
        
        fh.seek(0)
        with open(pdf_filename, "wb") as f:
            f.write(fh.read())
            
        print(f"Tool 'export_doc_as_pdf' SUCCESS: Saved as {pdf_filename}")
        return f"Successfully saved PDF as {pdf_filename}"
    except HttpError as error:
        print(f"Tool 'export_doc_as_pdf' ERROR: {error}")
        return f"Error exporting PDF: {error}"
    except Exception as e:
        print(f"Tool 'export_doc_as_pdf' UNEXPECTED ERROR: {e}")
        return f"An unexpected error occurred: {e}"