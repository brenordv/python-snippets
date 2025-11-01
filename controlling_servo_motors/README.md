# Controlling Servo Motors (Raspberry Pi + PCA9685)

This mini-project demonstrates how to control hobby servos using a Raspberry Pi (Zero W tested) and 
a SunFounder/Adafruit PCA9685 16‑Channel 12‑bit PWM driver via I²C. It provides two modes:
- Demo mode: runs automated motion patterns.
- Interactive mode: simple REPL to set servo angles on demand.

# Hardware
- Raspberry Pi Zero W
- SunFounder PCA9685 16‑Channel 12‑bit PWM Servo Driver (compatible with Adafruit PCA9685)
- 2x Miuzei 9G SG90 Micro Servos

> Why not connect the servos directly to the Pi?

Because I want to build a megazord some day, so using the PCA9685 as a driver is a good idea. 😂

# Quick start
- Repo path: `python-snippets/controlling_servo_motors`
- Entry point: `main.py`
- Servo channels used by default: `base_servo = 1`, `vert_servo = 2` (0‑based indexing for ServoKit)

# Setup
The project uses `uv` for dependency management and virtual environments, with dependencies declared in `pyproject.toml`
and locked in `uv.lock`.

Important: running on Raspberry Pi
- I²C must be enabled and the PCA9685 wired to the Pi. See Wiring + I²C below.
- The code uses `adafruit-circuitpython-servokit`, which pulls in `Adafruit-Blinka` to access hardware. This works on Raspberry Pi OS.
- The `pyproject.toml` currently specifies `requires-python = ">=3.13"`. If your Raspberry Pi image provides an older Python (common on Pi Zero W), either:
  - install Python 3.13+, or
  - temporarily loosen that constraint to match your installed Python (e.g., `>=3.9`) before syncing dependencies. (I don't see any reason why this would break anything, but it's not tested.)

## Install UV (one-time)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# then restart your shell or source your profile as prompted
```

## Set up the project environment
From the `controlling_servo_motors` folder on the Raspberry Pi:
1) Sync deps (creates a venv and installs packages):
```bash
uv sync
```
This reads `pyproject.toml` and `uv.lock` and installs `adafruit-circuitpython-servokit` and its deps.

2) Run the app through uv:
```bash
uv run python main.py demo
# or
uv run python main.py interactive
```

You can also activate the venv and run the app directly:
```bash
source .venv/bin/activate
python main.py demo
````

## Wiring + I²C on Raspberry Pi
- Power: Provide a separate 5V supply to the servos via the PCA9685 `V+` rail.
- PCA9685 power pins:
  - `V+` → external 5V servo power
  - `GND` → common ground (tie to Pi GND and external supply GND)
  - `VCC` → 3.3V from Pi (logic power for the PCA9685 board)
- I²C connections (Pi ↔ PCA9685):
  - Pi `SDA1` (GPIO 2, pin 3) → PCA9685 `SDA`
  - Pi `SCL1` (GPIO 3, pin 5) → PCA9685 `SCL`
  - Pi `GND` → PCA9685 `GND`
  - Pi `3V3` → PCA9685 `VCC`
- Default I²C address for PCA9685 is `0x40`.

## Enable I²C on Raspberry Pi
- Run `sudo raspi-config` → Interface Options → I2C → Enable → Reboot
- (Optional) Install tools and verify the board is seen at 0x40:
```bash
sudo apt update && sudo apt install -y i2c-tools
i2cdetect -y 1
```
> You should see `40` in the scan output.

How the code works
- `main.py` uses `ServoKit(channels=16)` to talk to the PCA9685 at the default address 0x40.
- Two channels are used:
  - `base_servo = 1`
  - `vert_servo = 2`

Interactive mode commands
At the prompt `>`, enter:
- `b <angle>` → set base servo to angle 0–180
- `v <angle>` → set vertical servo to angle 0–180
- `s <angle>` → set both servos to angle 0–180
- You can provide a comma-separated list to sequence moves, e.g. `b 0,45,90,135,180`
- `r` or `repeat` → repeat the previous command
- `q`/`quit`/`exit` → exit

Change servo channels or address
- To change channels, edit these lines near the top of `main.py`:
```python
base_servo = 1
vert_servo = 2
```
> Note: They are named like this because they are mounted in a kit with moving base and a vertical platform.

- If you changed the PCA9685 address via jumpers, initialize the kit like:
```python
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16, address=0x41)  # example address
```


Safety notes
- Always power servos from a suitable 5V supply; SG90s can stall and draw >500 mA each.
- Always share a common ground between the Pi, the PCA9685 board, and the servo power supply.
- Start moves at small increments and ensure mechanical limits aren’t exceeded.

Troubleshooting
- If `i2cdetect` doesn’t show 0x40: re-check wiring, enable I²C, and reboot.
- If imports fail, ensure the venv is active or use `uv run ...`.
- If angles don’t move as expected, verify channel numbers match your servo plugs on the PCA9685 block (0–15).