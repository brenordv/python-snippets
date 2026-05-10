"""CLI tool to decode and inspect JWT tokens without signature verification."""

import json
import sys
import argparse
from datetime import datetime, timezone

import jwt
from colorama import Fore, Style, init


def _get_command_line_arguments() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(description="Decode and inspect a JWT token.")
    parser.add_argument("token", nargs="+", help="JWT token string")
    parser.add_argument("--raw", "-r", action="store_true", help="Print raw decoded token")
    parser.add_argument("--json", "-j", action="store_true", help="Pretty print decoded token as JSON")
    return parser.parse_args()


def _sanitize_token(token: str) -> str:
    """Strip 'Bearer' prefix, whitespace, and newlines from a token string."""
    return token.replace("Bearer", "").replace(" ", "").replace("\n", "").replace("\r", "").strip()


def _decode_token(token: str) -> dict:
    """Decode a JWT token without verifying the signature."""
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.DecodeError as exc:
        print(f"Error decoding token: {exc}")
        sys.exit(1)


def _get_expiration_info(exp: int | None) -> tuple[str, str, str]:
    """Return (time_info, ansi_color, status) based on the 'exp' claim."""
    if exp:
        exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        time_diff = exp_datetime - now
        if time_diff.total_seconds() > 0:
            status = "Valid"
            color = Fore.GREEN
            time_left = str(time_diff).split(".")[0]
            time_info = f"expires in {time_left}"
        else:
            status = "Expired"
            color = Fore.RED
            time_left = str(-time_diff).split(".")[0]
            time_info = f"expired {time_left} ago"
    else:
        status = "No expiration claim"
        color = Fore.YELLOW
        time_info = ""

    return time_info, color, status


def _print_parsed_token(decoded_token: dict) -> None:
    """Print a human-readable summary of decoded JWT claims."""
    time_info, color, status = _get_expiration_info(decoded_token.get("exp"))
    print(f"{Style.BRIGHT}{color}{status}{Style.RESET_ALL}{Style.BRIGHT} - {time_info}{Style.RESET_ALL}")
    print(f"----{Style.BRIGHT}Claims:{Style.RESET_ALL}------------")
    for claim, value in decoded_token.items():
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        print(f"{claim}: {value}")


def main() -> None:
    """Entry point: parse arguments, decode the JWT, and display results."""
    init(autoreset=True)

    args = _get_command_line_arguments()
    token = _sanitize_token(" ".join(args.token))
    decoded_token = _decode_token(token)

    if args.raw:
        print(decoded_token)
    elif args.json:
        print(json.dumps(decoded_token, indent=4))
    else:
        _print_parsed_token(decoded_token)


if __name__ == "__main__":
    main()
