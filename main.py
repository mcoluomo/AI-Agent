import os
import sys

from dotenv import load_dotenv

from functions.get_files_info import (
    get_file_content,
    get_files_info,
    run_python_file,
    write_file,
)
from google import genai
from google.genai import types
from promp_call_function import available_functions, system_prompt


class FunctionCallError(Exception):
    pass


def main() -> None:
    load_dotenv()

    if len(sys.argv) == 1:
        print("Error: Please provide a prompt as a command-line argument.\n")
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    user_prompt = sys.argv[1]

    verbose = "--verbose" in sys.argv

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(20):
        response = generate_content(client, messages, verbose)
        for candidate in response.candidates:
            messages.append(candidate.content)

        if not response.function_calls:
            print("Final response:")
            print(response.text)
            break

        # Print function calls if present    # Print the main text/content response
        for function_call_part in response.function_calls:
            if verbose:
                print(f"Calling function: {function_call_part.name}")
            else:
                print(f"Calling function: {function_call_part.name}")

            function_call_result = call_function(function_call_part, verbose)

            messages.append(function_call_result)
            # Continue the loop - LLM will see function results and decide next step
        continue


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # Print the main text/content response

    return response


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_signatures = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in function_signatures:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                ),
            ],
        )

    function_call_args = dict(function_call_part.args)
    function_call_args["working_directory"] = "calculator"
    function_call = function_signatures[function_name]
    function_result = function_call(**function_call_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            ),
        ],
    )


if __name__ == "__main__":
    main()
