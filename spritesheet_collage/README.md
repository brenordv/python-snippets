# Spritesheet Collage

A small, dependency-light CLI tool to cut frames out of a spritesheet by grid coordinate and (optionally) stitch a 
chosen sequence into a new collage spritesheet. Handy for pulling an animation out of a sheet and re-ordering it,
creating an animation spritesheet strip.

## How it works

The spritesheet is treated as a grid of equally sized frames, with an optional **margin** (border on all four edges) 
and **separation** (gap between adjacentframes):

```
frame at (col, row) top-left = ( margin_x + col * (frame_x + sep_x),
                                 margin_y + row * (frame_y + sep_y) )
```

Coordinates are `[x, y]` = `[column, row]`, **0-based**: 
`[0,0]` is the top-left frame, 
`[1,0]` is the frame to its right,
`[0,1]` is the one below it.

> [!IMPORTANT]
> The tool refuses to run if the frame size, margin and separation do not divide the image into a whole number of 
> frames along either axis.

## Usage

```bash
# Cut the top row (4 frames) and stitch a ping-pong collage from them
uv run python spritesheet_collage.py test_spritesheet_64x64.png \
    --frame-x 64 --frame-y 64 \
    --frames "[[0,0],[1,0],[2,0],[3,0]]" \
    --collage "[1,2,3,4,3,2]"
```

This writes `frame_001__0_0.png` … `frame_004__3_0.png` plus a `collage.png` strip (`384x64`). 
Collage references are **1-based** (`1` = the first extracted frame) to make animation sequences easy to read.

### Interactive mode

Run with no arguments (or with some required values missing) to be prompted for each setting.
Inputs are validated immediately, so a typo in the spritesheet path or a bad coordinate list re-prompts only that field
instead of forcing the user to start over.

```bash
uv run python spritesheet_collage.py
```

### Arguments

| Argument                                     | Default      | Description                                 |
|----------------------------------------------|--------------|---------------------------------------------|
| `spritesheet`                                | - (required) | Path to the spritesheet image               |
| `--frame-x`, `--frame-y`                     | - (required) | Frame size in pixels                        |
| `--margin-x`, `--margin-y`                   | `0`          | Border around the whole sheet               |
| `--sep-x`, `--sep-y`                         | `0`          | Gap between adjacent frames                 |
| `--frames`                                   | - (required) | Frames to cut, e.g. `"[[0,0],[1,0]]"`       |
| `--collage`                                  | none         | 1-based stitch sequence, e.g. `"[1,2,3,2]"` |
| `--save-individual` / `--no-save-individual` | on           | Save each cut frame as a PNG                |
| `--frame-prefix`                             | `frame`      | Individual frame filename prefix            |
| `--collage-prefix`                           | `collage`    | Collage filename prefix                     |
| `--output-dir`                               | `.`          | Directory for output files                  |
| `-v`, `--verbose`                            | off          | Print per-frame detail                      |

Output filenames: `{frame-prefix}_{NNN}__{x}_{y}.png` for individual frames and `{collage-prefix}.png` for the collage.

## Running the tests

```bash
uv run python -m unittest discover
```

## Notes

- The collage is a single horizontal strip, one row of `frame_x × frame_y` cells.
- Per-frame transparency is preserved (output is RGBA PNG).
- List arguments are parsed with `ast.literal_eval`, so only plain Python literals are accepted (never arbitrary code).
