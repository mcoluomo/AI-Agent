import subprocess
import sys
from pathlib import Path

MAX_FILE_CONTENT_LENGTH = 9999


def get_files_info(working_directory, directory=None):
    """
    List files and directories within the specified directory under the working directory.

    Returns a formatted string with file names, sizes, and directory status, or an error string if the operation fails.
    """
    working_dir_path = Path(working_directory).resolve()

    if directory is None:
        directory = "."

    relative_path = Path(directory.lstrip("/"))
    resolved_target_path = (working_dir_path / relative_path).resolve()

    if not resolved_target_path.is_relative_to(working_dir_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not resolved_target_path.is_dir():
        return f'Error: "{directory}" is not a directory'
    contents_of_dir = ""
    try:
        for item in resolved_target_path.iterdir():
            size = item.stat().st_size

            contents_of_dir += (
                f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}\n"
            )

    except Exception as e:
        return f"Error: listing files: {e}"
    else:
        return contents_of_dir


def get_file_content(working_directory, file_path):
    """
    Read the content of a file within the given working directory.

    Returns the file content as a string, truncated if too long, or an error string if the operation fails.
    """
    working_dir_path = Path(working_directory).resolve()
    relative_path = Path(file_path.lstrip("/"))

    resolved_target_path = (working_dir_path / relative_path).resolve()

    if not resolved_target_path.is_relative_to(working_dir_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not resolved_target_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        content = resolved_target_path.read_text()
        if len(content) >= MAX_FILE_CONTENT_LENGTH:
            content = (
                content[:MAX_FILE_CONTENT_LENGTH]
                + f'\n[...File "{file_path}" truncated at 10000 characters]'
            )
    except Exception as e:
        return f'Error: reading file "{file_path}": {e}'
    else:
        return content


def write_file(working_directory, file_path, content):
    """
    Append content to a file within the given working directory.

    Returns a success message or an error string if the operation fails.
    """
    working_dir_path = Path(working_directory).resolve()
    relative_path = Path(file_path.lstrip("/"))

    resolved_target_path = (working_dir_path / relative_path).resolve()

    if not resolved_target_path.is_relative_to(working_dir_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    try:
        with Path(resolved_target_path).open("w") as fp:
            fp.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: file creation unsuccessfull {e}"


def run_python_file(working_directory, file_path, args=None):
    """
    Executes a Python file within the given working directory.
    Returns the combined stdout and stderr, or an error string.
    """
    working_dir_path = Path(working_directory).resolve()
    relative_path = Path(file_path.lstrip("/"))
    resolved_target_path = (working_dir_path / relative_path).resolve()

    if not resolved_target_path.is_relative_to(working_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not resolved_target_path.exists():
        return f'Error: File "{file_path}" not found.'
    if resolved_target_path.suffix != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    cmd = [sys.executable, str(resolved_target_path)]
    if args is not None:
        if isinstance(args, list):
            cmd.extend([str(arg) for arg in args])
        else:
            cmd.append(str(args))
    try:
        result = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."
    except Exception as e:
        return f"Error: executing Python file: {e}"

    stdout = result.stdout.decode().strip()
    stderr = result.stderr.decode().strip()
    output = ""

    if stdout:
        output += stdout + "\n"
    if stderr:
        output += stderr + "\n"

    if result.returncode != 0:
        output += f"Process exited with code {result.returncode}\n"
    if not output.strip():
        output = "No output produced."
    return output.strip()
