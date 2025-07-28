"""
Utility functions for file operations
"""
from pathlib import Path

def get_file_name_length(file_path: str | Path, include_suffix: bool = True) -> int:
    """
    Get the length of a file name
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return len(file_path.name) if include_suffix else len(file_path.stem)


def is_file_empty(file_path: str | Path) -> bool:
    """
    Check whether a file is empty
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.stat().st_size == 0 if file_path.is_file() else not any(file_path.iterdir())


def get_file_modification_date_timestamp(file_path: str | Path) -> int:
    """
    Get the timestamp of a file representing its last modification date
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.stat().st_mtime_ns


def get_file_size(file_path: str | Path) -> int:
    """
    Get the size of a file in bytes. Only works for files, not directories
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.stat().st_size


def get_file_type(file_path: str | Path) -> str:
    """
    Get the type of a file
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.suffix


def get_filtered_files(dir_path: str | Path, size_interval: tuple[int, int] | None = None, name_interval: tuple[int, int] | None = None,
                 date_interval: tuple[str, str] | None = None, file_types: list[str] | None = None, only_empty: bool = False) -> list[Path]:
    """
    Return a list containing files being part of the given directory and meeting the specified conditions
    """
    filtered_files: list[Path] = []

    if not isinstance(dir_path, Path):
        dir_path = Path(dir_path)

    if not dir_path.is_dir():
        raise NotADirectoryError(f'{dir_path} is not a directory')
    
    if date_interval:
        date_bounds = [get_file_modification_date_timestamp(date_str) for date_str in date_interval]
    else:
        date_bounds = None 

    for file_path in dir_path.glob('**/*'):
            file_path_stat = file_path.stat()

            if only_empty:
                if file_path_stat.st_size != 0:
                    continue
            else:
                if size_interval and not size_interval[0] <= file_path_stat.st_size <= size_interval[1]:
                    continue
            if name_interval and not name_interval[0] <= get_file_name_length(file_path) <= name_interval[1]:
                continue
            if date_bounds:
                if not date_bounds[0] <= file_path_stat.st_mtime <= date_bounds[1]:
                    continue
            if file_types and not get_file_type(file_path) in file_types:
                continue

            filtered_files.append(file_path)

    return filtered_files