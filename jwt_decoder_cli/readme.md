# JWT Decoder CLI

Command-line tool to decode and inspect JWT tokens without verifying the signature. Displays claims with color-coded expiration status (green for valid, red for expired, yellow for missing expiration).

## Usage

```bash
# Default: human-readable claims with expiration status
python jwtr.py eyJhbGciOiJIUzI1NiIs...

# Accepts 'Bearer' prefix and spaces
python jwtr.py Bearer eyJhbGciOiJIUzI1NiIs...

# Raw decoded dict
python jwtr.py --raw eyJhbGciOiJIUzI1NiIs...

# Pretty-printed JSON
python jwtr.py --json eyJhbGciOiJIUzI1NiIs...
```
