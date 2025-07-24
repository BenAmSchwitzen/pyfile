"""
CLI entry point — receives and parses CLI commands for file operations.
"""
import argparse


parser = argparse.ArgumentParser(
    description='pyfile — CLI tool for deleting, searching, renaming, copying and moving files.'
)

subparsers = parser.add_subparsers(dest='command', help='Available commands')

delete_parser = subparsers.add_parser(
    'delete',
    aliases=['del'],
    help='Delete files being part of the given directories based on specified conditions',
    usage='pyfile delete <dir_path_1> ... <dir_path_i> [--size MIN MAX] [--name MIN MAX] [--date DD.MM.YY  DD.MM.YY] [--file_types FILE_TYPE_1 ... FILE_TYPE_i] [--only_empty]',
)

delete_parser.add_argument('dir_paths', nargs='+', help='Directories that will be scanned for files to be deleted', type=str)
delete_parser.add_argument('--size', nargs=2, metavar=('MIN', 'MAX'), type=int, help='Delete files whose size is within the given interval', default=None)
delete_parser.add_argument('--name', nargs=2, metavar=('MIN', 'MAX'), type=int, help='Delete files whose name length is within the given interval', default=None)
delete_parser.add_argument('--date', nargs=2, metavar=('START', 'END'), help='Delete files created within the given interval', default=None)
delete_parser.add_argument('--file_types', nargs='+', metavar=('types', 'type_1'), help='Files whose type is not in the list will be ignored', default=None)
delete_parser.add_argument('--only_empty', action='store_true', help='Ignore sizing conditions and delete only empty files')
