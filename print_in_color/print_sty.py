"""Demo of colored terminal output using the sty package."""

from sty import bg, ef, fg, rs

# Error / Warning / Success messages
print(fg.red + "ERROR Test!" + fg.rs)
print(fg.li_yellow + "WARNING Test!" + fg.rs)
print(fg.green + "SUCCESS Test!" + fg.rs)

# Background and italic
print(bg.blue + "This has a powershell-blue background!" + bg.rs)
print(ef.italic + "This is italic text" + rs.italic)

# Custom color via RGB
fg.orange = ("rgb", (255, 150, 50))
print(fg.orange + "Hey apple!" + fg.rs)
