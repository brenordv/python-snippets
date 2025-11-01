import sys

from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

base_servo = 1
vert_servo = 2

def main_interactive():
    # Simple command UI:
    # - b <angle>  -> set base servo to angle (0-180)
    # - v <angle>  -> set vertical servo to angle (0-180)
    # - s <angle>  -> set both to angle (0-180)
    # - q          -> quit
    print("Interactive mode. Commands: 'b <angle>', 'v <angle>', 's <angle>', 'r' to repeat last command, 'q' to quit.")
    print(f"Current servos: base={base_servo}, vert={vert_servo}")
    try:
        previous_command = None
        while True:
            try:
                cmd = input("> ").strip().lower()
                if not cmd:
                    continue

                # Quit
                if cmd in ("q", "quit", "exit"):
                    print("Exiting...")
                    break

                # Repeat the previous command
                if cmd in ("r", "repeat"):
                    if previous_command:
                        print(f"Repeating: {previous_command}")
                        cmd = previous_command
                    else:
                        print("No previous command to repeat.")
                        continue
                else:
                    previous_command = cmd

                # Parse command
                parts = cmd.split()
                if len(parts) == 2 and parts[0] in ("b", "v", "s"):
                    target = parts[0].lower()
                    try:
                        angles_text = parts[1]

                        if "," in angles_text:
                            angles = [int(angle) for angle in angles_text.split(",")]
                        else:
                            angles = [int(parts[1])]
                    except ValueError:
                        print("Angle must be an integer 0-180.")
                        continue

                    for angle in angles:
                        # Clamp angle
                        clamped_angle = max(0, min(180, angle))
                        if target == "b":
                            kit.servo[base_servo].angle = clamped_angle
                            print(f"Base -> {clamped_angle}")
                        elif target == "v":
                            kit.servo[vert_servo].angle = clamped_angle
                            print(f"Vert -> {clamped_angle}")
                        else:  # "s" both
                            kit.servo[base_servo].angle = clamped_angle
                            kit.servo[vert_servo].angle = clamped_angle
                            print(f"Both -> {clamped_angle}")

                        time.sleep(0.3)
                else:
                    print("Unknown command. Use: 'b 90', 'v 45', 's 120', or 'q'.")
                time.sleep(0.05)
            except Exception as e:
                # Handle unexpected errors without stopping the loop
                print(f"Error: {e}")
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping gracefully.")

def main_demo():
    while True:
        print("Bringing them back to zero")
        kit.servo[base_servo].angle = 0
        kit.servo[vert_servo].angle = 0

        print("Moving base")
        for x in range(4):
            for i in range(0, 180, 4):
                kit.servo[base_servo].angle = i
                time.sleep(0.05)

            for i in range(180, 0, -4):
                kit.servo[base_servo].angle = i
                time.sleep(0.05)

        print("Moving vertical")
        for x in range(4):
            for i in range(0, 180, 4):
                kit.servo[vert_servo].angle = i
                time.sleep(0.05)

            for i in range(180, 0, -4):
                kit.servo[vert_servo].angle = i
                time.sleep(0.05)

        print("Bringing them back to zero")
        kit.servo[base_servo].angle = 0
        kit.servo[vert_servo].angle = 0
        time.sleep(0.05)

        for i in range(0, 180, 10):
            kit.servo[base_servo].angle = i
            kit.servo[vert_servo].angle = i
            time.sleep(0.05)

        print("Waiting 3 seconds")
        time.sleep(3)


def main():
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
    # Usage: python main.py [demo|interactive]
    main()