# Python Snippets

A collection of self-contained Python snippets, examples, and small utilities.

## Getting Started

Each snippet lives in its own directory with a `pyproject.toml` describing its
dependencies. The recommended way to run any snippet is with
[uv](https://docs.astral.sh/uv/):

```bash
# Run a snippet directly (uv handles the virtual environment and dependencies)
cd snippet_directory
uv run python script_name.py

# Or create a virtual environment first
cd snippet_directory
uv sync
uv run python script_name.py
```

If you don't have `uv` installed:

```bash
# Install uv (macOS / Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install uv (Windows)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Snippets

| Snippet                                                                   | Description                                                              |
|---------------------------------------------------------------------------|--------------------------------------------------------------------------|
| [argparse_demo](argparse_demo/)                                           | Demonstration of argparse usage with various argument types              |
| [cache_func_execution](cache_func_execution/)                             | Benchmark comparing cached vs uncached Fibonacci using `functools.cache` |
| [check_is_number](check_is_number/)                                       | Two approaches for validating whether user input is a number             |
| [controlling_servo_motors](controlling_servo_motors/)                     | Control hobby servos using a Raspberry Pi and PCA9685 PWM driver         |
| [demo_terminal_colors](demo_terminal_colors/)                             | Demonstration of ANSI terminal color codes                               |
| [elapsed_time](elapsed_time/)                                             | Utility to compute and display formatted elapsed time                    |
| [exit_script](exit_script/)                                               | Two approaches for cleanup on script exit: `atexit` and `try/finally`    |
| [extract_lines](extract_lines/)                                           | Extract lines matching a search term from a file                         |
| [file_renaming](file_renaming/)                                           | Batch-rename files matching a three-part naming pattern                  |
| [fun_with_dates](fun_with_dates/)                                         | Date parsing, uptime calculation, and relative dates                     |
| [get_addr_by_cep](get_addr_by_cep/)                                       | Progressive examples of Brazilian postal code (CEP) lookups              |
| [get_computer_info](get_computer_info/)                                   | Collect system health metrics and publish to MQTT                        |
| [get_path](get_path/)                                                     | Retrieve the current script's directory at runtime                       |
| [getter_setter_demo](getter_setter_demo/)                                 | Python property decorators for getter/setter validation                  |
| [import_from_dir](import_from_dir/)                                       | Importing modules from a directory using packages                        |
| [jwt_decoder_cli](jwt_decoder_cli/)                                       | CLI tool to decode and inspect JWT tokens                                |
| [kaprekar_routine](kaprekar_routine/)                                     | Demonstrate the Kaprekar Routine converging to 6174                      |
| [misc](misc/)                                                             | Miscellaneous snippets: version checking, dictionary init                |
| [obtain_google_oauth2_refresh_token](obtain_google_oauth2_refresh_token/) | Exchange a Google OAuth2 code for a refresh token                        |
| [open_ai_generate_image_and_resize](open_ai_generate_image_and_resize/)   | Generate images with DALL-E and resize with Pillow                       |
| [pass_dynamic_args_to_func](pass_dynamic_args_to_func/)                   | Different ways to pass dynamic arguments to functions                    |
| [print_in_color](print_in_color/)                                         | Colored terminal output using sty, termcolor, and ANSI codes             |
| [remove_duplicates](remove_duplicates/)                                   | Remove duplicate dictionaries from a list                                |
| [serialize_datetime](serialize_datetime/)                                 | Serialize datetime objects to JSON                                       |
| [spinning_cursor](spinning_cursor/)                                       | Spinning cursor animation for terminal output                            |
| [split_strip](split_strip/)                                               | Split a string and strip whitespace: loop vs comprehension               |
| [web_scraping_simple_example](web_scraping_simple_example/)               | Scrape Azure resource naming conventions to Markdown                     |
| [xml_using_xpath](xml_using_xpath/)                                       | Extract XML data using XPath with xml.etree and lxml                     |

## License

See [LICENSE](LICENSE) for details.
