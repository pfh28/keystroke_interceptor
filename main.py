# This is a sample Python script.
import selectors

from pynput import keyboard


class KeyEvent:
    def __init__(self, event, key):
        self.event = event
        self.key = key

    def __eq__(self, other):
        return self.event == other.event and self.key == other.key

# variables for dealing with replaying events
event_buffer = []
pressed_keys = set()
exit_flag = False

#variables for tracking state and dealing with musescoren
dial_mode = "duration"

def switch_dial_mode():
    global dial_mode
    if dial_mode == "duration":
        dial_mode = "position"
        print("\n"*10)
        print("""\
  _____   ____   _____ _____ _______ _____ ____  _   _ 
 |  __ \ / __ \ / ____|_   _|__   __|_   _/ __ \| \ | |
 | |__) | |  | | (___   | |    | |    | || |  | |  \| |
 |  ___/| |  | |\___ \  | |    | |    | || |  | | . ` |
 | |    | |__| |____) |_| |_   | |   _| || |__| | |\  |
 |_|     \____/|_____/|_____|  |_|  |_____\____/|_| \_|nnnnn
                """)
    else:
        dial_mode = "duration"
        print("\n" * 10)
        print("""\
          _____                  _   _             
         |  __ \                | | (_)            
         | |  | |_   _ _ __ __ _| |_ _  ___  _ __  
         | |  | | | | | '__/ _` | __| |/ _ \| '_ \ 
         | |__| | |_| | | | (_| | |_| | (_) | | | |
         |_____/ \__,_|_|  \__,_|\__|_|\___/|_| |_|                                       
        """)


def get_right_turn():
    if dial_mode == "duration":
        return keyboard.Key.f13
    else:
        return keyboard.Key.right


def get_left_turn():
    if dial_mode == "duration":
        return keyboard.Key.f14
    else:
        return keyboard.Key.left


passthrough = keyboard.Controller()
def on_press(key):
    if key == keyboard.Key.media_volume_up:
#        print(get_right_turn())
        event_buffer.append(KeyEvent("down", get_right_turn()))
        event_buffer.append(KeyEvent("up", get_right_turn()))
    elif key == keyboard.Key.media_volume_down:
#        print(get_left_turn())
        event_buffer.append(KeyEvent("down", get_left_turn()))
        event_buffer.append(KeyEvent("up", get_left_turn()))
    elif key == keyboard.Key.media_volume_mute:
        print("mode switch")
        switch_dial_mode()
    else:
#        print('key {0} pressed'.format(
#            key))
        event_buffer.append(KeyEvent("down", key))
        pressed_keys.add(key)


def on_release(key):
    global exit_flag
    if key != keyboard.Key.media_volume_up and key != keyboard.Key.media_volume_down and key != keyboard.Key.media_volume_mute:
        event_buffer.append(KeyEvent("up", key))
        try:
            pressed_keys.remove(key)
        except:
            print("failed to remove key ", key)
        print('{0} released'.format(
            key))

    if key == keyboard.Key.esc:
        # Stop listener
        exit_flag = True

    if len(pressed_keys) == 0:
        return False


while not exit_flag:
    # Collect events until released
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True) as listener:


            listener.join()

            for event in event_buffer:
                if event.event == "down":
                    passthrough.press(event.key)
                else:
                    passthrough.release(event.key)
            event_buffer = []
