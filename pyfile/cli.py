"""
CLI entry point — receives and parses CLI commands for file operations.
"""
import argparse

parser = argparse.ArgumentParser(
    description='PyFile — CLI tool for organizing, copying, sorting, moving and deleting files.'
)

subparsers = parser.add_subparsers(dest='command', help='Available commands')