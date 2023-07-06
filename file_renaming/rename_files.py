# -*- coding: utf-8 -*-
import os
import re

"""
rename_file.py: This utility provides a Python function rename_files() to rename all files in a specified directory 
that match a particular pattern. 

"""

__author__ = "Breno RdV"
__copyright__ = "Breno RdV @ raccoon.ninja"
__contact__ = "https://raccoon.ninja"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Breno RdV"
__status__ = "Demonstration"


def rename_files(path, dry_run=True):
    """
    This function renames all files in the specified path that match the pattern 'First part - Second part - Third part.<any_extension>'.
    The renamed files have the ' - Third part' removed from their names.

    Args:
    path (str): The directory path where the files to be renamed are located.
    dry_run (bool): If True, the function will only print the changes that would be made, without renaming any files.

    Returns:
    None
    """

    # Loop through each file in the specified directory
    for filename in os.listdir(path):
        # Check if the filename matches the pattern 'First part - Second part - Third part.<any_extension>'
        if not re.match(r'.* - .* - .*\..*', filename):
            continue

        # Split the filename into parts
        parts = filename.split(' - ')  # Split by ' - '

        # Check if the filename has at least 3 parts
        if len(parts) < 3:
            # This should not be necessary, considering that the filename was matched by the regex above.
            print(f"File '{filename}' does not match the pattern: First part - Second part - Third part.<any_extension>")
            continue

        # Get the file extension from the third part
        extension = parts[-1].split('.', 1)[1]

        # Construct the new filename using the first two parts and the extension
        # Replace spaces with underscores and add '__' between the first and second parts
        new_name = f'{parts[0]}__{parts[1]}.{extension}'.replace(' ', '_')

        # Construct absolute paths for the old and new filenames
        old_file = os.path.join(path, filename)
        new_file = os.path.join(path, new_name)

        # If this is a dry run, just print the changes that would be made
        if dry_run:
            print(f'Would rename: {old_file} -> {new_file}')

        else:
            # Otherwise, rename the file
            os.rename(old_file, new_file)


if __name__ == '__main__':
    rename_files(path="c:\\path\\to\\files", dry_run=True)
