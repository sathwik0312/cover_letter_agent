# create_cover_letter.py
import argparse
import asyncio
from google.adk.runners import Runner
from cover_letter_agent.agent import cover_letter_agent  # <-- Import your agent definition
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async
session_service = InMemorySessionService()

from dotenv import load_dotenv
load_dotenv()

async def main():
    parser = argparse.ArgumentParser(description="Cover Letter Generation Agent")
    parser.add_argument("--role", type=str, required=True)
    parser.add_argument("--company", type=str, required=True)
    args = parser.parse_args()

    print(f"🚀 Starting Cover Letter Agent for {args.role} at {args.company}...")
    APP_NAME="support agent"
    USER_ID = "sathwik3"

    initial_state={
    "user_name":"sathwik",
    "COMPANY_NAME":args.company,
    "ROLE_NAME":args.role,
    }

    # ===== PART 3: Session Creation =====
    # Create a new session with initial state
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )
    SESSION_ID = new_session.id
    # This is the ADK runner
    runner = Runner(
        agent=cover_letter_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    user_prompt_text = f"Create a cover letter for the role of '{args.role}' at '{args.company}'."
    await call_agent_async(runner, USER_ID, SESSION_ID, user_prompt_text)
    # The prompt that triggers the agent's instructions
    

if __name__ == "__main__":
    # This will run the first time and ask you to authenticate
    # with Google in your browser.
    asyncio.run(main())