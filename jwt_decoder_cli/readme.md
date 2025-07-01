# Attention
I recreated this tool using Rust: https://github.com/brenordv/rusted-toolbox

# JWT Token Decoder (`jwtr.py`)

This script decodes the public data of a JWT (JSON Web Token) and provides information about its validity and claims. It can display the token in various formats based on the provided command-line arguments.

## Features

- **Decode JWT Tokens**: Extract and display the claims from a JWT.
- **Token Validity Check**: Determine if the token is valid or expired based on the `exp` claim.
- **Color-Coded Output**:
  - **Valid Tokens**: Displayed in **green** with time until expiration.
  - **Expired Tokens**: Displayed in **red** with time since expiration.
- **Flexible Output Formats**:
  - **Default**: Prints claims line by line.
  - **Raw Decoded Token**: Use `--raw` or `-r` to display the raw decoded JSON.
  - **Pretty-Printed JSON**: Use `--json` to display the claims in a formatted JSON.

## Prerequisites

- **Python 3.x**
- **Required Python Packages**:
  - `PyJWT`
  - `colorama`

## Installation

### 1. Download the Script

Save the `jwtr.py` script to a directory of your choice.

### 2. Install Required Packages

Open your terminal and run:

```bash
pip install PyJWT colorama
```

If you have multiple versions of Python, you may need to use `pip3`:

```bash
pip3 install PyJWT colorama
```

## Making the Script Executable

To turn `jwtr.py` into an executable script on Linux or macOS, follow these steps:

### 1. Add Execute Permissions

Navigate to the directory containing `jwtr.py` and run:

```bash
chmod +x jwtr.py
```

### 2. Ensure the Shebang Line is Correct

The script already includes the shebang line:

```python
#!/usr/bin/env python3
```

This line tells the system to execute the script using Python 3.

### 3. Move the Script to a Directory in Your PATH (Optional)

To run the script from any location without specifying the path, move it to a directory that's in your `PATH`, such as `/usr/local/bin`:

```bash
sudo mv jwtr.py /usr/local/bin/jwtr
```

**Note**: We renamed the script to `jwtr` (without the `.py` extension) for convenience.

## Usage

```bash
jwtr [OPTIONS] <token>
```

### Options

- `--raw`, `-r`: Print the raw decoded token.
- `--json`, '-j': Pretty-print the decoded token in JSON format.

### Arguments

- `<token>`: The JWT token string to decode. The token can include the word `Bearer` and may contain spaces or line breaks, which the script will remove automatically.

### Examples

#### 1. Default Usage

```bash
jwtr eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 2. Token with 'Bearer' and Spaces

```bash
jwtr Bearer eyJhbGciOiJIUzI1NiIs InR5cCI6IkpXVCJ9...
```

#### 3. Raw Decoded Token

```bash
jwtr --raw eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 4. Pretty-Printed JSON

```bash
jwtr --json eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Output Format

### Validity Status

- **Valid Tokens**: Printed in **green** with the time remaining until expiration.
  ```
  Valid - expires in 0:59:59
  ```
- **Expired Tokens**: Printed in **red** with the time since expiration.
  ```
  Expired - expired 0:10:00 ago
  ```

### Claims Display

- **Default**: Each claim is printed on a new line in the format `claim: value`.
- **Lists**: If a claim's value is a list, the values are joined by commas.
  ```
  roles: admin,user,editor
  ```

## Troubleshooting

- **Module Not Found Errors**:
  - If you encounter errors like `ModuleNotFoundError: No module named 'jwt'` or `No module named 'colorama'`, ensure you've installed the required packages:
    ```bash
    pip install PyJWT colorama
    ```

- **Permission Denied**:
  - If you get a permission error when moving the script to `/usr/local/bin`, use `sudo`:
    ```bash
    sudo mv jwtr.py /usr/local/bin/jwtr
    ```

- **Python Version Issues**:
  - Ensure that `python3` is installed and correctly referenced in the shebang line.
  - You can check your Python version with:
    ```bash
    python3 --version
    ```

## Notes

- The script ignores any occurrences of `Bearer`, spaces, or line breaks in the token input.
- It uses the `exp` claim to determine token validity.
- If the `exp` claim is missing, it will display a warning in yellow:
  ```
  No expiration claim
  ```

## Requirements

- **PyJWT**: A Python library for encoding and decoding JWTs.
- **Colorama**: A library to produce colored terminal text.
