"""
Set the game resolution to 1280x720 and enable windowed mode.
Make sure the attack arrow icon is set to show all.
Bring up the mine page and set the desired units before starting the script.
After the script starts, you have 5 seconds to focus on the game window.
Update mine_stage.png and deltas as necessary. mine_stage.png should show the stage number icon.
"""

import time
import random
import pyautogui
from pynput import keyboard

module_have = 75
module_want_to_leave = 30
n = (module_have - module_want_to_leave) // 3   # the number of times to play the stage

stage_confidence_lower_bound = 0.7   # increase if getting too many false positives


last_pressed = None
def on_press(key):
    global last_pressed
    last_pressed = key
def check_key_interrupt():
    # stop if r key or q key is pressed
    if last_pressed in [keyboard.KeyCode.from_char('r'), keyboard.KeyCode.from_char('q')]:
        print("Quitting script...")
        listener.stop()
        quit(0)

print("Script starts in 5 seconds...")
time.sleep(5)

# Start the listener to quit at any time
listener = keyboard.Listener(on_press)
kb = keyboard.Controller()
print("Starting listening...")
listener.start()

for i in range(n):
    print(f"Stage count: {i+1}/{n}")
    # Start mining stage
    print("Starting the mining stage...")
    # decrement confidence until an image is found
    # play with the upper bound until it doesn't give too many false positives
    stage_location = None
    stage_confidence = 0.95  # starting value
    while stage_location is None and stage_confidence >= stage_confidence_lower_bound:
        try:
            print(f"Attempting to locate mine stage with confidence {stage_confidence}...")
            stage_location = pyautogui.locateOnScreen('mine_stage.png', confidence=stage_confidence)
        except pyautogui.ImageNotFoundException:
            stage_confidence -= 0.05
    if stage_location is None:
        raise pyautogui.ImageNotFoundException("image not found even at minimum confidence")
    time.sleep(0.5)
    dx = 50
    dy = 280
    pyautogui.click(stage_location.left + dx, stage_location.top + dy)
    time.sleep(random.random() + 0.3)
    pyautogui.press('enter')

    # Move mouse out of the way for the loop
    pyautogui.moveTo(stage_location.left - 300, stage_location.top)

    # Wait for stage start
    print("Waiting for stage start...")
    while True:
        check_key_interrupt()
        try:
            pyautogui.locateOnScreen('arrows.png', confidence=0.9)
            print("Stage start detected")
            break
        except pyautogui.ImageNotFoundException:
            time.sleep(3)

    # Autoplay until game finished
    print("Auto play started")
    while True:
        check_key_interrupt()
        try:
            # Stage done if stage icon can be found
            stage_confidence = 0.95
            stage_location = None
            while stage_location is None and stage_confidence >= stage_confidence_lower_bound:
                try:
                    print(f"Attempting to locate mine stage with confidence {stage_confidence}...")
                    stage_location = pyautogui.locateOnScreen('mine_stage.png', confidence=stage_confidence)
                except pyautogui.ImageNotFoundException:
                    stage_confidence -= 0.05
            if stage_location is None:
                raise pyautogui.ImageNotFoundException("image not found even at minimum confidence")
            print("Stage end detected")
            break
        except pyautogui.ImageNotFoundException:
            pyautogui.press('p')
            time.sleep(0.5 + random.random() * 0.25)
            pyautogui.press('enter')
            time.sleep(3 + random.random() * 0.5)
