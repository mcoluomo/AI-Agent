from pathlib import Path


def get_files_info(working_directory, directory=None):
    working_dir_path = Path(working_directory)
    relative_path = Path(directory)

    resolved_target_path = (working_dir_path / relative_path).resolve()
    try:
        resolved_target_path.is_relative_to(working_dir_path)

        if not resolved_target_path.exists():
            return f'Error: Directory "{directory}" does not exist'
        if not resolved_target_path.is_dir():
            return f'Error: "{directory}" is not a directory'

        contends_of_dir = ""
        for item in resolved_target_path.iterdir():

                size = item.stat().st_size
                contends_of_dir += (
                    f"- {item.name}: file_size={size} bytes, is_dir={item.is_dir()}\n"
                )
    except OSError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    return contends_of_dir
