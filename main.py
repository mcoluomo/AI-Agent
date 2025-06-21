import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types

if len(sys.argv) == 1:
    print("Error: Please provide a prompt as a command-line argument.")
    sys.exit(1)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)


print(response)

VERBOSE_ARG_INDEX = 2
print(
    "User prompt: "
    if len(sys.argv) > VERBOSE_ARG_INDEX and sys.argv[VERBOSE_ARG_INDEX] == "--verbose"
    else "",
    sys.argv[1],
)

print(
    f"{'Prompt tokens: ' if len(sys.argv) > VERBOSE_ARG_INDEX and sys.argv[VERBOSE_ARG_INDEX] == '--verbose' else ''} {response.usage_metadata.prompt_token_count}",
) if response.usage_metadata is not None else print("No usage metadata available.")


print(
    f"{'Response tokens: ' if len(sys.argv) > VERBOSE_ARG_INDEX and sys.argv[VERBOSE_ARG_INDEX] == '--verbose' else ''}{response.usage_metadata.candidates_token_count}",
) if response.usage_metadata is not None else print("No usage metadata available.")
