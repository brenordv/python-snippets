"""Extract frames from a spritesheet and optionally stitch them into a collage.

Run with command-line arguments for one-shot use, or with missing/no arguments
to fall back to an interactive prompt that validates each value immediately.

Example:
    python spritesheet_collage.py test_spritesheet_64x64.png \
        --frame-x 64 --frame-y 64 \
        --frames "[[0,0],[1,0],[2,0],[3,0]]" \
        --collage "[1,2,3,4,3,2]"
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, UnidentifiedImageError

# A pathological collage sequence could request a multi-gigabyte canvas; cap the
# total number of cells so the tool fails fast with a clear message instead of
# exhausting memory.
MAX_COLLAGE_CELLS = 4096


@dataclass(frozen=True)
class Geometry:
    """Pixel layout of a spritesheet grid.

    Frames are laid out with a margin border on all four edges and an optional
    separation gap between adjacent frames. The top-left pixel of the frame at
    grid ``(col, row)`` is ``(margin_x + col * (frame_x + sep_x), ...)``.
    """

    frame_x: int
    frame_y: int
    margin_x: int = 0
    margin_y: int = 0
    sep_x: int = 0
    sep_y: int = 0


@dataclass(frozen=True)
class Config:
    """Fully resolved run configuration (after CLI parsing or interactive input)."""

    spritesheet: Path
    geometry: Geometry
    frames_to_cut: list[tuple[int, int]]
    collage: list[int]
    save_individual: bool
    frame_prefix: str
    collage_prefix: str
    output_dir: Path
    verbose: bool


# --------------------------------------------------------------------------- #
# Pure parsing / validation helpers (unit-testable, no I/O)
# --------------------------------------------------------------------------- #
def parse_frames(raw: str) -> list[tuple[int, int]]:
    """Parse a ``"[[0,0],[1,0]]"`` string into a list of ``(col, row)`` pairs.

    Args:
        raw: A string holding a Python literal list of ``[int, int]`` pairs.

    Returns:
        The parsed list of integer coordinate tuples.

    Raises:
        ValueError: If the string is not a list of two-integer pairs.
    """
    value = _literal_eval(raw)
    if not isinstance(value, list) or not value:
        raise ValueError("Frames must be a non-empty list, e.g. [[0,0],[1,0]].")

    frames: list[tuple[int, int]] = []
    for item in value:
        if (
            not isinstance(item, (list, tuple))
            or len(item) != 2
            or not all(isinstance(coord, int) for coord in item)
        ):
            raise ValueError(
                f"Each frame must be an [x, y] integer pair; got {item!r}."
            )
        frames.append((int(item[0]), int(item[1])))
    return frames


def parse_collage(raw: str, frame_count: int) -> list[int]:
    """Parse a ``"[1,2,3,2]"`` string into a list of 1-based frame references.

    Args:
        raw: A string holding a Python literal list of integers.
        frame_count: Number of extracted frames the references must point into.

    Returns:
        The parsed list of 1-based indices (empty if ``raw`` is blank).

    Raises:
        ValueError: If the string is not a list of integers within range, or
            the sequence exceeds ``MAX_COLLAGE_CELLS``.
    """
    if not raw or not raw.strip():
        return []

    value = _literal_eval(raw)
    if not isinstance(value, list) or not value:
        raise ValueError("Collage must be a non-empty list, e.g. [1,2,3,2].")
    if not all(isinstance(item, int) for item in value):
        raise ValueError("Collage entries must all be integers.")
    if len(value) > MAX_COLLAGE_CELLS:
        raise ValueError(
            f"Collage sequence too long ({len(value)} > {MAX_COLLAGE_CELLS})."
        )

    for ref in value:
        if not 1 <= ref <= frame_count:
            raise ValueError(
                f"Collage reference {ref} is out of range; expected 1..{frame_count}."
            )
    return list(value)


def _literal_eval(raw: str):
    """Safely evaluate a Python literal, raising a friendly ValueError on failure."""
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError, TypeError) as exc:
        raise ValueError(f"Could not parse {raw!r}: {exc}") from exc


def compute_grid(image_width: int, image_height: int, geom: Geometry) -> tuple[int, int]:
    """Compute the number of (columns, rows) of frames in a spritesheet.

    Args:
        image_width: Spritesheet width in pixels.
        image_height: Spritesheet height in pixels.
        geom: The grid geometry.

    Returns:
        A ``(n_cols, n_rows)`` tuple.

    Raises:
        ValueError: If the geometry does not divide the image into a whole
            number of frames along either axis.
    """
    n_cols = _frames_along_axis(
        image_width, geom.frame_x, geom.margin_x, geom.sep_x, axis="X"
    )
    n_rows = _frames_along_axis(
        image_height, geom.frame_y, geom.margin_y, geom.sep_y, axis="Y"
    )
    return n_cols, n_rows


def _frames_along_axis(length: int, frame: int, margin: int, sep: int, axis: str) -> int:
    """Return the whole number of frames along one axis or raise ValueError."""
    # length = 2*margin + n*frame + (n-1)*sep  =>  n = (length - 2*margin + sep) / (frame + sep)
    numerator = length - 2 * margin + sep
    denominator = frame + sep
    if numerator <= 0 or numerator % denominator != 0:
        remainder = numerator % denominator
        raise ValueError(
            f"Frame size + margin + separation do not yield a whole number of "
            f"frames along {axis} (axis length {length}px leaves {remainder}px "
            f"remaining)."
        )
    return numerator // denominator


def frame_box(col: int, row: int, geom: Geometry) -> tuple[int, int, int, int]:
    """Return the ``(left, top, right, bottom)`` crop box for grid cell (col, row)."""
    left = geom.margin_x + col * (geom.frame_x + geom.sep_x)
    top = geom.margin_y + row * (geom.frame_y + geom.sep_y)
    return left, top, left + geom.frame_x, top + geom.frame_y


def safe_prefix(prefix: str) -> str:
    """Validate that a filename prefix is a single path component.

    Args:
        prefix: The user-supplied prefix.

    Returns:
        The prefix unchanged if it is safe.

    Raises:
        ValueError: If the prefix contains path separators or is ``.``/``..``.
    """
    if not prefix or Path(prefix).name != prefix or prefix in (".", ".."):
        raise ValueError(
            f"Invalid filename prefix {prefix!r}: must not contain path separators."
        )
    return prefix


# --------------------------------------------------------------------------- #
# Imaging (I/O)
# --------------------------------------------------------------------------- #
def extract_frames(
    image: Image.Image, frames_to_cut: list[tuple[int, int]], grid: tuple[int, int], geom: Geometry
) -> list[Image.Image]:
    """Crop the requested grid cells out of the spritesheet.

    Args:
        image: The opened spritesheet image.
        frames_to_cut: List of ``(col, row)`` coordinates to extract.
        grid: The ``(n_cols, n_rows)`` grid size, used for bounds checking.
        geom: The grid geometry.

    Returns:
        Cropped frames in the same order as ``frames_to_cut``.

    Raises:
        ValueError: If any coordinate falls outside the grid.
    """
    n_cols, n_rows = grid
    frames: list[Image.Image] = []
    for col, row in frames_to_cut:
        if not (0 <= col < n_cols and 0 <= row < n_rows):
            raise ValueError(
                f"Frame [{col}, {row}] is outside the {n_cols}x{n_rows} grid."
            )
        frames.append(image.crop(frame_box(col, row, geom)))
    return frames


def build_collage(frames: list[Image.Image], sequence: list[int], geom: Geometry) -> Image.Image:
    """Stitch a 1-based frame sequence into a single horizontal strip.

    Args:
        frames: The extracted frames (extraction order).
        sequence: 1-based indices into ``frames`` defining the strip order.
        geom: The grid geometry (frame dimensions).

    Returns:
        A new RGBA image of size ``(len(sequence) * frame_x, frame_y)``.
    """
    collage = Image.new("RGBA", (len(sequence) * geom.frame_x, geom.frame_y))
    for position, ref in enumerate(sequence):
        frame = frames[ref - 1].convert("RGBA")
        collage.paste(frame, (position * geom.frame_x, 0), frame)
    return collage


def open_spritesheet(path: Path) -> Image.Image:
    """Open and fully load a spritesheet, raising a friendly error on failure."""
    try:
        with Image.open(path) as image:
            image.load()
            return image.copy()
    except FileNotFoundError:
        raise ValueError(f"Spritesheet not found: {path}")
    except Image.DecompressionBombError as exc:
        raise ValueError(f"Spritesheet is too large to process safely: {exc}")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError(f"Could not read spritesheet {path}: {exc}")


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def save_outputs(frames: list[Image.Image], config: Config) -> list[Path]:
    """Save individual frames and/or the collage according to ``config``.

    Returns:
        The list of file paths written.
    """
    config.output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    if config.save_individual:
        for number, ((col, row), frame) in enumerate(
            zip(config.frames_to_cut, frames), start=1
        ):
            name = f"{config.frame_prefix}_{number:03d}__{col}_{row}.png"
            path = config.output_dir / name
            _warn_if_overwriting(path)
            frame.save(path)
            written.append(path)
            if config.verbose:
                print(f"  saved frame {number:03d} ({col},{row}) -> {path}")

    if config.collage:
        collage = build_collage(frames, config.collage, config.geometry)
        path = config.output_dir / f"{config.collage_prefix}.png"
        _warn_if_overwriting(path)
        collage.save(path)
        written.append(path)
        if config.verbose:
            print(f"  saved collage {collage.size[0]}x{collage.size[1]} -> {path}")

    return written


def _warn_if_overwriting(path: Path) -> None:
    """Print a stderr notice when an output file already exists."""
    if path.exists():
        print(f"Note: overwriting existing file {path}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _get_command_line_arguments() -> argparse.Namespace:
    """Parse command-line arguments (all optional, to allow interactive fallback)."""
    parser = argparse.ArgumentParser(
        description="Extract spritesheet frames and optionally stitch a collage."
    )
    parser.add_argument("spritesheet", nargs="?", help="Path to the spritesheet image.")
    parser.add_argument("--frame-x", type=int, help="Frame width in pixels.")
    parser.add_argument("--frame-y", type=int, help="Frame height in pixels.")
    parser.add_argument("--margin-x", type=int, default=0, help="Left/right border (default 0).")
    parser.add_argument("--margin-y", type=int, default=0, help="Top/bottom border (default 0).")
    parser.add_argument("--sep-x", type=int, default=0, help="Horizontal gap between frames (default 0).")
    parser.add_argument("--sep-y", type=int, default=0, help="Vertical gap between frames (default 0).")
    parser.add_argument("--frames", help='Frames to cut, e.g. "[[0,0],[1,0]]".')
    parser.add_argument("--collage", help='1-based stitch sequence, e.g. "[1,2,3,2]".')
    parser.add_argument(
        "--save-individual",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Save each extracted frame as a PNG (default: on).",
    )
    parser.add_argument("--frame-prefix", default="frame", help="Individual frame prefix (default 'frame').")
    parser.add_argument("--collage-prefix", default="collage", help="Collage filename prefix (default 'collage').")
    parser.add_argument("--output-dir", default=".", help="Directory for output files (default: current dir).")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print per-frame detail.")
    return parser.parse_args()


def _has_all_required(args: argparse.Namespace) -> bool:
    """Return True when every required value is present on the command line."""
    return all(
        value is not None
        for value in (args.spritesheet, args.frame_x, args.frame_y, args.frames)
    )


def _validate_geometry_values(frame_x, frame_y, margin_x, margin_y, sep_x, sep_y) -> Geometry:
    """Build a Geometry, enforcing positive frame sizes and non-negative spacing."""
    if frame_x <= 0 or frame_y <= 0:
        raise ValueError("Frame width and height must be positive.")
    if min(margin_x, margin_y, sep_x, sep_y) < 0:
        raise ValueError("Margins and separations must not be negative.")
    return Geometry(frame_x, frame_y, margin_x, margin_y, sep_x, sep_y)


def _resolve_from_args(args: argparse.Namespace) -> Config:
    """Build a Config directly from complete command-line arguments."""
    geometry = _validate_geometry_values(
        args.frame_x, args.frame_y, args.margin_x, args.margin_y, args.sep_x, args.sep_y
    )
    spritesheet = Path(args.spritesheet)
    if not spritesheet.is_file():
        raise ValueError(f"Spritesheet not found: {spritesheet}")

    frames = parse_frames(args.frames)
    collage = parse_collage(args.collage or "", len(frames))
    save_individual = args.save_individual
    if not save_individual and not collage:
        raise ValueError(
            "Nothing to do: individual saving is off and no collage was requested."
        )
    return Config(
        spritesheet=spritesheet,
        geometry=geometry,
        frames_to_cut=frames,
        collage=collage,
        save_individual=save_individual,
        frame_prefix=safe_prefix(args.frame_prefix),
        collage_prefix=safe_prefix(args.collage_prefix),
        output_dir=Path(args.output_dir),
        verbose=args.verbose,
    )


# --------------------------------------------------------------------------- #
# Interactive mode
# --------------------------------------------------------------------------- #
def _prompt(message: str, default: str | None = None) -> str:
    """Prompt for a value, returning the default on an empty response."""
    suffix = f" [{default}]" if default else ""
    while True:
        answer = input(f"{message}{suffix}: ").strip()
        if answer:
            return answer
        if default is not None:
            return default


def _prompt_with(parse, message: str, default: str | None = None):
    """Prompt and re-prompt until ``parse`` accepts the input (no restart on typo)."""
    while True:
        try:
            return parse(_prompt(message, default))
        except ValueError as exc:
            print(f"  {exc}", file=sys.stderr)


def _resolve_interactive(args: argparse.Namespace) -> Config:
    """Gather configuration interactively, validating each value immediately."""
    print("Interactive mode — press Enter to accept the [default].\n")

    spritesheet = _prompt_with(
        _existing_file, "Spritesheet path", args.spritesheet
    )
    frame_x = _prompt_with(_positive_int, "Frame width (px)", _as_str(args.frame_x))
    frame_y = _prompt_with(_positive_int, "Frame height (px)", _as_str(args.frame_y))
    margin_x = _prompt_with(_non_negative_int, "Margin X (px)", str(args.margin_x))
    margin_y = _prompt_with(_non_negative_int, "Margin Y (px)", str(args.margin_y))
    sep_x = _prompt_with(_non_negative_int, "Separation X (px)", str(args.sep_x))
    sep_y = _prompt_with(_non_negative_int, "Separation Y (px)", str(args.sep_y))
    geometry = Geometry(frame_x, frame_y, margin_x, margin_y, sep_x, sep_y)

    frames = _prompt_with(parse_frames, "Frames to cut, e.g. [[0,0],[1,0]]", args.frames)
    collage = _prompt_with(
        lambda raw: parse_collage(raw, len(frames)),
        "Collage sequence (1-based, blank to skip), e.g. [1,2,3,2]",
        args.collage or "",
    )
    save_individual = _prompt_with(
        _yes_no, "Save individual frames? (y/n)", "y" if args.save_individual else "n"
    )
    if not save_individual and not collage:
        print("  Nothing to do; enabling individual saving.", file=sys.stderr)
        save_individual = True

    frame_prefix = _prompt_with(safe_prefix, "Frame filename prefix", args.frame_prefix)
    collage_prefix = _prompt_with(safe_prefix, "Collage filename prefix", args.collage_prefix)
    output_dir = _prompt("Output directory", args.output_dir)

    return Config(
        spritesheet=Path(spritesheet),
        geometry=geometry,
        frames_to_cut=frames,
        collage=collage,
        save_individual=save_individual,
        frame_prefix=frame_prefix,
        collage_prefix=collage_prefix,
        output_dir=Path(output_dir),
        verbose=args.verbose,
    )


def _as_str(value) -> str | None:
    """Render an optional argument value as a default string."""
    return None if value is None else str(value)


def _existing_file(raw: str) -> str:
    if not Path(raw).is_file():
        raise ValueError(f"File not found: {raw}")
    return raw


def _positive_int(raw: str) -> int:
    value = _non_negative_int(raw)
    if value <= 0:
        raise ValueError("Value must be positive.")
    return value


def _non_negative_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"{raw!r} is not an integer.")
    if value < 0:
        raise ValueError("Value must not be negative.")
    return value


def _yes_no(raw: str) -> bool:
    lowered = raw.strip().lower()
    if lowered in ("y", "yes"):
        return True
    if lowered in ("n", "no"):
        return False
    raise ValueError("Please answer 'y' or 'n'.")


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def _print_run_summary(config: Config, grid: tuple[int, int]) -> None:
    """Echo the resolved configuration before doing any work."""
    n_cols, n_rows = grid
    print(
        f"Spritesheet: {config.spritesheet} (grid {n_cols}x{n_rows}, "
        f"frame {config.geometry.frame_x}x{config.geometry.frame_y})"
    )
    print(
        f"Cutting {len(config.frames_to_cut)} frame(s); "
        f"collage: {config.collage or 'none'}; "
        f"save individual: {config.save_individual}; output dir: {config.output_dir}"
    )


def run(config: Config) -> list[Path]:
    """Execute the extraction/collage pipeline and return written paths."""
    image = open_spritesheet(config.spritesheet)
    grid = compute_grid(image.width, image.height, config.geometry)
    _print_run_summary(config, grid)

    frames = extract_frames(image, config.frames_to_cut, grid, config.geometry)
    written = save_outputs(frames, config)

    print(f"\nDone. Wrote {len(written)} file(s):")
    for path in written:
        print(f"  {path}")
    return written


def main() -> None:
    """Entry point: resolve configuration (CLI or interactive) and run."""
    args = _get_command_line_arguments()
    try:
        config = _resolve_from_args(args) if _has_all_required(args) else _resolve_interactive(args)
        run(config)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
