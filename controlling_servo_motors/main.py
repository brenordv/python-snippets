"""Control hobby servos via a PCA9685 PWM driver on Raspberry Pi.

Provides two modes:
- demo: automated motion patterns
- interactive: REPL to set servo angles on demand
"""

import sys
import time

from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

BASE_SERVO = 1
VERT_SERVO = 2


def main_interactive() -> None:
    """Run an interactive REPL for setting servo angles."""
    print(
        "Interactive mode. Commands: 'b <angle>', 'v <angle>', "
        "'s <angle>', 'r' to repeat last command, 'q' to quit."
    )
    print(f"Current servos: base={BASE_SERVO}, vert={VERT_SERVO}")

    try:
        previous_command: str | None = None
        while True:
            try:
                cmd = input("> ").strip().lower()
                if not cmd:
                    continue

                if cmd in ("q", "quit", "exit"):
                    print("Exiting...")
                    break

                if cmd in ("r", "repeat"):
                    if previous_command:
                        print(f"Repeating: {previous_command}")
                        cmd = previous_command
                    else:
                        print("No previous command to repeat.")
                        continue
                else:
                    previous_command = cmd

                parts = cmd.split()
                if len(parts) == 2 and parts[0] in ("b", "v", "s"):
                    target = parts[0]
                    try:
                        angles_text = parts[1]
                        if "," in angles_text:
                            angles = [int(a) for a in angles_text.split(",")]
                        else:
                            angles = [int(parts[1])]
                    except ValueError:
                        print("Angle must be an integer 0-180.")
                        continue

                    for angle in angles:
                        clamped = max(0, min(180, angle))
                        if target == "b":
                            kit.servo[BASE_SERVO].angle = clamped
                            print(f"Base -> {clamped}")
                        elif target == "v":
                            kit.servo[VERT_SERVO].angle = clamped
                            print(f"Vert -> {clamped}")
                        else:
                            kit.servo[BASE_SERVO].angle = clamped
                            kit.servo[VERT_SERVO].angle = clamped
                            print(f"Both -> {clamped}")
                        time.sleep(0.3)
                else:
                    print("Unknown command. Use: 'b 90', 'v 45', 's 120', or 'q'.")

                time.sleep(0.05)
            except Exception as exc:
                print(f"Error: {exc}")
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping gracefully.")


def main_demo() -> None:
    """Run automated servo motion patterns in a loop."""
    while True:
        print("Bringing them back to zero")
        kit.servo[BASE_SERVO].angle = 0
        kit.servo[VERT_SERVO].angle = 0

        print("Moving base")
        for _ in range(4):
            for i in range(0, 180, 4):
                kit.servo[BASE_SERVO].angle = i
                time.sleep(0.05)
            for i in range(180, 0, -4):
                kit.servo[BASE_SERVO].angle = i
                time.sleep(0.05)

        print("Moving vertical")
        for _ in range(4):
            for i in range(0, 180, 4):
                kit.servo[VERT_SERVO].angle = i
                time.sleep(0.05)
            for i in range(180, 0, -4):
                kit.servo[VERT_SERVO].angle = i
                time.sleep(0.05)

        print("Bringing them back to zero")
        kit.servo[BASE_SERVO].angle = 0
        kit.servo[VERT_SERVO].angle = 0
        time.sleep(0.05)

        for i in range(0, 180, 10):
            kit.servo[BASE_SERVO].angle = i
            kit.servo[VERT_SERVO].angle = i
            time.sleep(0.05)

        print("Waiting 3 seconds")
        time.sleep(3)


def main() -> None:
    """Parse the mode argument and dispatch to the appropriate function."""
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: python main.py [demo|interactive]")
        sys.exit(2)

    mode = args[0].lower()
    if mode == "demo":
        main_demo()
    elif mode == "interactive":
        main_interactive()
    else:
        print("Error: unknown mode. Use 'demo' or 'interactive'.")
        sys.exit(2)


if __name__ == "__main__":
    main()
