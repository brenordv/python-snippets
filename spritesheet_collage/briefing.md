# Briefing
The idea here is to have a local, simple tool to extract spritesheet frames, and (optionally) stitch them together into 
a new spritesheet.

When using this the user must pass:
1. The target spritesheet file: self explanatory
2. Frame size X: self explanatory
3. Frame size Y: self explanatory
4. Spritesheet Margin X (Default: 0)
5. Spritesheet Margin Y (Default: 0)
6. Frame Separation X (Default: 0)
7. Frame Separation Y (Default: 0)
8. Frames to cut: list with frame coordinates to cut from the spritesheet. Example: [[0,0],[1,0],[0,1],[1,1]] will cut the top left, top right, bottom left and bottom right frames.
  - This can be passed as a string, and parsed in a secure manner (without over-engineering this)
  - [0,0] means the frame in the first row and column, while [9, 9] means the frame in the 10th row and column.
9. Collage: Number of frames you cut that will be stitched together into a new spritesheet.
  - Example: 
    - Consider that we extracted a "walk animation" from these frames: [[0,0],[1,0],[2,0],[3,0]]
    - And this animation is configured in a "ping-pong" style
    - So the collage values would be: [1, 2, 3, 4, 3, 2]
      - In this sequence, 1 means the first frame we extracted (0, 0), and 4 means the fourth frame we extracted (3, 0).
    - Collage is base 1 to make it easier for us (humans) to think about the animation sequence.
    - This can be passed as a string, and parsed in a secure manner (without over-engineering this)
10. If we should save the individual frames (Default: true)
11. Individual frame filename prefix (Default: frame)
  - The frame filename pattern will be {prefix}_{frame_number with 3 digits}__{frame X coordinate}_{frame Y coordinate}.png
12. Collage filename prefix (Default: collage)
    
The app will alert the user if the frame size X + spritesheet margin X + frame separation X doesn't result in an "integer number of frames".
Same validation will be done to the Y values.

The values can be passed all in one go via CLI arguments, or with a nice cli interactive setting if the user either doesn't pass all the required values or just runs the script without any args.

Before start to work, the script must validate if the target spritesheet exists.
While in interactive mode, this can be immediate, so if the user makes a typo, they don't need to start all over again.

If you need, we have a test spritesheet in the folder called `test_spritesheet_64x64.png` containing 64 frames of 64x64 pixels.

# Strategy
1. Do not mention this document. It will not be shipped with the snippet.
2. Try to keep to this as simple as possible. We don't want a full-fledged long term scalable application now. Just a quick, useful, and maintainable script.
3. Keep the code as simple as possible, and don't over-engineer it.
4. Avoid using external libraries or dependencies, if possible. But if it is reasonable to use them, do so.
5. Use the full-work workflow for this.