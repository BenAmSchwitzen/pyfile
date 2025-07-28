"""
This module provides functions for file operations
"""
from pathlib import Path
import utils
import shutil

def delete_files(dir_paths: list[str], size_interval: tuple[int, int] | None = None, name_interval: tuple[int, int] | None = None,
                 date_interval: tuple[str, str] | None = None, file_types: list[str] | None = None, only_empty: bool = False) -> None:
    """
    Delete files being part of the given directory paths based on specified conditions
    """
    for directory_path in dir_paths:
        directory_path = Path(directory_path)

        if not directory_path.is_dir():
            raise NotADirectoryError(f'{directory_path} is not a directory')

        if date_interval:
            date_bounds = [utils.get_file_modification_date_timestamp(date_str) for date_str in date_interval]
        else:
            date_bounds = None
            
        for file_path in directory_path.glob('**/*'):
            file_path_stat = file_path.stat()

            if only_empty:
                if file_path_stat.st_size != 0:
                    continue
            else:
                if size_interval and not size_interval[0] <= file_path_stat.st_size <= size_interval[1]:
                    continue
            if name_interval and not name_interval[0] <= utils.get_file_name_length(file_path) <= name_interval[1]:
                continue
            if date_bounds:
                if not date_bounds[0] <= file_path_stat.st_mtime <= date_bounds[1]:
                    continue
            if file_types and not utils.get_file_type(file_path) in file_types:
                continue

            try:
                if file_path.is_file():
                    file_path.unlink()
                else:
                    shutil.rmtree(file_path)
            except Exception:
                print(f'Failed to delete {file_path} of {directory_path}')


def filter_files(dir_path: str | Path, size_interval: tuple[int, int] | None = None, name_interval: tuple[int, int] | None = None,
                 date_interval: tuple[str, str] | None = None, file_types: list[str] | None = None, only_empty: bool = False, 
                 mark: str | None = None, move: str | None = None, delete: bool = False) -> None:
    """
    Filter files based on specified conditions and perform a specified action

    Supported actions (choose only one):
    - mark: Appends the specified string to each filtered file's stem
    - move: Moves the filtered files to a target directory
    - delete: Deletes the filtered files
    """
    filter_actions: list[bool] = [bool(mark), bool(move), delete]
    if sum(filter_actions) > 1:
        raise ValueError('You are not allowed to specify more than one of the following actions: mark, move, delete')

    filtered_files: list[Path] = []

    if not isinstance(dir_path, Path):
        dir_path = Path(dir_path)

    if not dir_path.is_dir():
        raise NotADirectoryError(f'{dir_path} is not a directory')
    
    if date_interval:
        date_bounds = [utils.get_file_modification_date_timestamp(date_str) for date_str in date_interval]
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
            if name_interval and not name_interval[0] <= utils.get_file_name_length(file_path) <= name_interval[1]:
                continue
            if date_bounds:
                if not date_bounds[0] <= file_path_stat.st_mtime <= date_bounds[1]:
                    continue
            if file_types and not utils.get_file_type(file_path) in file_types:
                continue

            filtered_files.append(file_path)

    if mark:
        for file_path in filtered_files:
            file_path.rename(file_path.with_stem(file_path.stem + mark))
    elif move:
        dest_directory_path = Path(move)
        if not dest_directory_path.is_dir():
            raise NotADirectoryError(f'{move} is not a directory and therefore cannot be used as a destination')
        for file_path in filtered_files:
            file_path.rename(dest_directory_path / file_path.name)
    elif delete:
        for file_path in filtered_files:
            try:
                if file_path.is_file():
                    file_path.unlink()
                else:
                    shutil.rmtree(file_path)
            except Exception:
                print(f'Failed to delete {file_path.name} of {dir_path}')         