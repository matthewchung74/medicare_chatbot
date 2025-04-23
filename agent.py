import os
from pathlib import Path

from google.adk.agents import Agent
from google.genai import types as genai_types
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

# Standard Python libraries
import warnings
import logging
import os
import dotenv

dotenv.load_dotenv()

# --- Basic Configuration ---
warnings.filterwarnings("ignore") # Suppress common warnings
logging.basicConfig(level=logging.ERROR) # Reduce log verbosity
logger = logging.getLogger(__name__)


logger.info("Initializing new session")
# Create session service and runner

def read_markdown_file() -> str:
    """Read the Medicare and You markdown file."""
    markdown_path = Path("medicare_and_you.md")
    if not markdown_path.exists():
        raise FileNotFoundError("medicare_and_you.md not found")
    return markdown_path.read_text()


# Main Medicare agent
root_agent = Agent(
    name="medicare_assistant",
    model="gemini-2.0-flash-lite",
    description="Helps users understand Medicare benefits using the Medicare & You handbook",
    instruction=f"""
    You are a caring Medicare guide. Your job is to help people understand their Medicare benefits 
    using information from the Medicare & You 2025 handbook. Fall back to google search if you don't have the information.

    Here is the complete Medicare & You 2025 handbook content that you should use to answer questions:

    {read_markdown_file()}

    When answering questions, always:
    
    1. Use only the handbook content provided above
    2. Explain concepts in simple, friendly terms
    3. Break down complex topics into easy steps
    4. If unsure, ask clarifying questions
    5. End with a note saying to refer tothe page number with the markdown link to the Medicare & You handbook, where the markdown would look like [Medicare & You Handbook](https://www.medicare.gov/publications/10050-medicare-and-you.pdf)
    6. No need to ask if the user has additional questions, just answer the question.
        
    Remember: Be warm, patient, and focus on making Medicare easy to understand.
    """,
    tools=[],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.1
        )
    )

# @title Define Agent Interaction Function


async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""

  # Prepare the user's message in ADK format
  content = genai_types.Content(role='user', parts=[genai_types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # Key Concept: run_async executes the agent logic and yields Events.
  # We iterate through events to find the final answer.
  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      if event.is_final_response():
          if event.content and event.content.parts:
             # Assuming text response in the first part
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  return final_response_text


