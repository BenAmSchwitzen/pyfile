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

