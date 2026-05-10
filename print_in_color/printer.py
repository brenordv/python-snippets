"""Simple colored console printer using ANSI escape codes (no dependencies)."""


class Printer:
    """Print messages to the console with ANSI color codes."""

    COLORS: dict[str, str] = {
        **dict.fromkeys(("RED", "ERROR", "NO"), "\033[1;31m"),
        **dict.fromkeys(("GREEN", "OK", "YES"), "\033[0;32m"),
        **dict.fromkeys(("YELLOW", "WARN", "MAYBE"), "\033[0;93m"),
        "BLUE": "\033[1;34m",
        "CYAN": "\033[1;36m",
        "RESET": "\033[0;0m",
        "BOLD": "\033[;1m",
        "REVERSE": "\033[;7m",
    }

    def _get_color(self, key: str) -> str:
        """Return the ANSI escape code for *key*, falling back to RESET."""
        return self.COLORS.get(key, self.COLORS["RESET"])

    def print(self, msg: str, color: str = "RESET") -> None:
        """Print *msg* wrapped in the ANSI code for *color*."""
        ansi = self._get_color(key=color)
        print(f"{ansi}{msg}{self.COLORS['RESET']}")

    def error(self, msg: str) -> None:
        """Print *msg* in red."""
        self.print(msg=msg, color="RED")

    def success(self, msg: str) -> None:
        """Print *msg* in green."""
        self.print(msg=msg, color="GREEN")

    def warning(self, msg: str) -> None:
        """Print *msg* in yellow."""
        self.print(msg=msg, color="YELLOW")


if __name__ == "__main__":
    p = Printer()
    p.success("SUCCESS Test...")
    p.warning("WARN Test...")
    p.error("ERROR Test...")
