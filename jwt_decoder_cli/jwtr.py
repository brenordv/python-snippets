#!/usr/bin/env python3
# Required packages:
# pip install PyJWT colorama

import sys
import base64
import json
import argparse
from datetime import datetime, timezone
import jwt  # PyJWT
from colorama import init, Fore, Style


def _get_command_line_arguments():
    parser = argparse.ArgumentParser(description='Process a JWT token.')
    parser.add_argument('token', nargs='+', help='JWT token string')
    parser.add_argument('--raw', '-r', action='store_true', help='Print raw decoded token')
    parser.add_argument('--json', '-j', action='store_true', help='Pretty print decoded token')

    return parser.parse_args()


def _sanitize_token(token):
    return token.replace('Bearer', '').replace(' ', '').replace('\n', '').replace('\r', '').strip()


def _decode_token(token):
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return decoded_token
    except jwt.DecodeError as e:
        print(f"Error decoding token: {e}")
        sys.exit(1)


def _get_expiration_info(exp):
    if exp:
        exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        now = datetime.now(timezone.utc)
        time_diff = exp_datetime - now
        if time_diff.total_seconds() > 0:
            status = 'Valid'
            color = Fore.GREEN
            time_left = str(time_diff).split('.')[0]
            time_info = f"expires in {time_left}"
        else:
            status = 'Expired'
            color = Fore.RED
            time_left = str(-time_diff).split('.')[0]
            time_info = f"expired {time_left} ago"
    else:
        status = 'No expiration claim'
        color = Fore.YELLOW
        time_info = ''

    return time_info, color, status


def _print_parsed_token(decoded_token):
    time_info, color, status = _get_expiration_info(decoded_token.get('exp'))
    print(f"{Style.BRIGHT}{color}{status}{Style.RESET_ALL}{Style.BRIGHT} - {time_info}{Style.RESET_ALL}")
    print(f"----{Style.BRIGHT}Claims:{Style.RESET_ALL}------------")
    for claim, value in decoded_token.items():
        if isinstance(value, list):
            value = ','.join(map(str, value))
        print(f"{claim}: {value}")


def main():
    # Reset styles, colors, etc.
    init(autoreset=True)

    # Get command line arguments
    args = _get_command_line_arguments()

    # Join token parts and clean it. The token might have spaces and/or the word Bearer.
    token = _sanitize_token(' '.join(args.token))

    # Decode token
    decoded_token = _decode_token(token)

    if args.raw:
        # Prints raw decoded token
        print(decoded_token)
    elif args.json:
        # Pretty print decoded token
        print(json.dumps(decoded_token, indent=4))
    else:
        # Print parsed decoded token
        _print_parsed_token(decoded_token)


if __name__ == '__main__':
    main()
