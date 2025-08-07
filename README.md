# AI-Agent
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/mcoluomo/AI-Agent)

This repository contains an AI coding agent that leverages the Google Gemini Pro model's function-calling capabilities to interact with a local file system. The agent can understand user prompts, analyze a codebase, read files, write changes, and execute Python scripts to accomplish tasks within a sandboxed environment.

The primary example included is a simple command-line calculator, which the agent can debug, modify, and test based on natural language instructions.

## Features

- **File System Interaction**: The agent can list files and directories.
- **File Content Analysis**: It has the ability to read the contents of any file within its designated working directory.
- **Code Execution**: The agent can run Python scripts and analyze their output (stdout/stderr).
- **Code Modification**: It can write new content to files or overwrite existing ones.
- **Sandboxed Environment**: All file operations are restricted to a specific working directory (`calculator/`) for security, preventing unintended access to the broader file system.
- **Iterative Problem-Solving**: The agent can make multiple function calls in a sequence to gather information, test hypotheses, and arrive at a solution.

## Getting Started

### Prerequisites

- Python 3.x
- A Google Gemini API Key

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mcoluomo/AI-Agent.git
    cd AI-Agent
    ```

2.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project directory and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

## Usage

Run the agent from the command line, providing your request as a string argument. The agent will then formulate a plan and begin executing function calls to fulfill the request.

### Basic Usage

```sh
python main.py "Your prompt here"
```

### Examples

**Ask the agent to run the calculator's tests and report the result:**
```sh
python main.py "Can you run the tests for the calculator and tell me if they pass?"
```

**Ask the agent to fix a bug in the calculator:**
```sh
python main.py "The calculator does not handle order of operations correctly. For '2 + 3 * 4', it should be 14, not 20. Please fix it."
```

**Ask the agent a question about the codebase:**
```sh
python main.py "What does the render.py file in the calculator's pkg directory do?"
```

### Verbose Mode

For a more detailed output, including the model's thoughts, token counts, and full function call details, use the `--verbose` flag.

```sh
python main.py "Your prompt here" --verbose
```

## How It Works

1.  **User Prompt**: The `main.py` script captures the user's command-line prompt.
2.  **Model Interaction**: The prompt is sent to the Gemini model along with a system instruction and a list of available tools (functions). These tools are defined in `functions/get_files_info.py` with their corresponding schemas in `promp_call_function.py`.
3.  **Function Calling**: The model analyzes the request and, if necessary, responds with a request to call one of the available functions (e.g., `get_file_content` to read a file).
4.  **Local Execution**: The script executes the requested function call locally. All file paths are interpreted relative to the secure `calculator/` working directory.
5.  **Feedback Loop**: The output of the function (e.g., file content or script execution result) is sent back to the model as part of the ongoing conversation.
6.  **Iteration**: The model continues this process—analyzing results and calling functions—until it has enough information to solve the user's request.
7.  **Final Response**: Once the task is complete, the model provides a final textual response summarizing what it did and the outcome.
