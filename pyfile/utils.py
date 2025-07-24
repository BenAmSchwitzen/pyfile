"""
Utility functions for file operations
"""

from pathlib import Path
import os

def get_file_size(file_path: str | Path) -> int:
    """
    Get the size of a file in bytes. Only works for files, not directories
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.stat().st_size

def get_file_name_length(file_path: str | Path, include_suffix: bool = True) -> int:
    """
    Get the length of a file name
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return len(file_path.name) if include_suffix else len(file_path.stem)

def get_file_creation_date_timestamp(file_path: str | Path) -> int:
    """
    Get the timestamp of a file representing its creation date
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    stat = file_path.stat()
    if os.name == 'nt':
        # On Windows = ctime
        return stat.st_ctime_ns
    else:
        try:
            return stat.st_birthtime_ns
        except AttributeError:
            return stat.st_mtime_ns
        
def get_file_modification_date_timestamp(file_path: str | Path) -> int:
    """
    Get the timestamp of a file representing its last modification date
    """
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    return file_path.stat().st_mtime_ns

def is_empty_dir(dir_path: str | Path) -> bool:
    """
    Check if a directory is empty
    """
    if not isinstance(dir_path, Path):
        dir_path = Path(dir_path)
    return not any(dir_path.iterdir())