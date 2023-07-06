# File Renaming Utility

This utility provides a Python function `rename_files()` to rename all files in a specified directory that match a 
particular pattern. The pattern it's looking for is `First part - Second part - Third part.<any_extension>`. The renamed
files will have the ' - Third part' removed from their names.

## Usage

Import the function into your Python script and call it as shown below:

```python
from rename_files import rename_files

# Call the function specifying the path and whether it's a dry-run
rename_files('/path/to/your/files', dry_run=True)
```

The `dry_run` parameter is optional. If set to `True`, the function will only print the changes that would be made, 
without renaming any files. This can be useful to verify the results before making actual changes. If omitted or set 
to `False`, the function will rename the files.


## Caveats

- The function will only rename files, not directories. 
- The function uses the Python `os.rename()` function, which will overwrite any existing files without warning. So if a
file with the new name already exists, it will be replaced by the renamed file.
- For dry-run mode, it only prints the changes that would be made. It does not perform any checks to see if the 
renaming would be successful (e.g. permission issues, disk space).
- The function assumes that there is only one '.' in the filename, which is used to separate the filename and the 
extension. Filenames with multiple '.' may not be handled correctly.
- Please make sure to back up your files before running this function, just in case something unexpected happens.


## Disclaimer

This script is provided "as is", without warranty of any kind, express or implied. Please use it at your own risk. 
Always backup your data before running any scripts that modify it.