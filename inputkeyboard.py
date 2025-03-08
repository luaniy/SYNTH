import keyboard

if __name__ == "__main__":
    keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))