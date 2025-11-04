"""
`game_state` module

All variables in this module can be read AND set by any file, and changes to variables update across all files. 
This is good because it allows modules to communicate with each other without risking circular imports.

`level_running` - bool: Whether the level is running or not. Used to stop recursive tasks for the level (e.g. obstacle spawning).
"""

level_running = False