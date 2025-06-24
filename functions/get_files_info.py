import subprocess
import sys
from pathlib import Path

MAX_FILE_CONTENT_LENGTH = 9999


def get_files_info(working_directory, directory=None):
    working_dir_path = Path(working_directory).resolve()

    if directory is None:
        directory = "."

    relative_path = Path(directory.lstrip("/"))
    resolved_target_path = (working_dir_path / relative_path).resolve()

    if not resolved_target_path.is_relative_to(working_dir_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not resolved_target_path.is_dir():
        return f'Error: "{directory}" is not a directory'
    contends_of_dir = ""
    try:
        for item in resolved_target_path.iterdir():
            size = item.stat().st_size

            contends_of_dir += (
                f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}\n"
            )

    except Exception as e:
        return f"Error: listing files: {e}"
    else:
        return contends_of_dir


def get_file_content(working_directory, file_path):
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
        return f"Error: listing files: {e}"
    else:
        return content


def write_file(working_directory, file_path, content):
    working_dir_path = Path(working_directory).resolve()
    relative_path = Path(file_path.lstrip("/"))

    resolved_target_path = (working_dir_path / relative_path).resolve()

    if not resolved_target_path.is_relative_to(working_dir_path):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    try:
        with Path(resolved_target_path).open("a") as fp:
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

    try:
        cmd = [sys.executable, str(resolved_target_path)]
        if args is not None:
            if isinstance(args, list):
                cmd.extend([str(arg) for arg in args])
            else:
                cmd.append(str(args))
        result = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            timeout=30,
            check=False,
        )
        stdout = result.stdout.decode().strip()
        stderr = result.stderr.decode().strip()
        output = ""
        if stdout:
            output += f"STDOUT:\n{stdout}\n"
        if stderr:
            output += f"STDERR:\n{stderr}\n"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if not output:
            output = "No output produced."
        return output
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."
    except Exception as e:
        return f"Error: executing Python file: {e}"
