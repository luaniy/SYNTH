#Input keyboard testing

import keyboard

keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))