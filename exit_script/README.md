# Exit Script

Two approaches for running cleanup code when a Python script exits. `using_at_exit.py` registers a callback with the `atexit` module, while `using_try_catch.py` uses a `try/except/finally` block to ensure cleanup runs.

## Usage

```bash
# Using atexit
python using_at_exit.py

# Using try/except/finally
python using_try_catch.py
```
