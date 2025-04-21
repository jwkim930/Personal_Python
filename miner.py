"""
Set the game resolution to 1280x720 and enable windowed mode.
Make sure the attack arrow icon is set to show all.
Bring up the mine page and set the desired units before starting the script.
After the script starts, you have 5 seconds to focus on the game window.
Update mine_stage.png and deltas as necessary. mine_stage.png should show the stage number icon.
"""

import time
import pyautogui
from pynput import keyboard

n = 1   # the number of times to play the stage


last_pressed = None
def on_press(key):
    global last_pressed
    last_pressed = key
def check_key_interrupt():
    # stop if r key is pressed
    if last_pressed == keyboard.KeyCode.from_char('r'):
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
    print("Stage count:", i+1)
    # Start mining stage
    print("Starting the mining stage...")
    stage_location = pyautogui.locateOnScreen('mine_stage.png', confidence=0.9)
    dx = 50
    dy = 300
    pyautogui.click(stage_location.left + dx, stage_location.top + dy)
    time.sleep(0.5)
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

    # Auto play until game finished
    print("Auto play started")
    while True:
        check_key_interrupt()
        try:
            # Stage done if stage icon can be found
            pyautogui.locateOnScreen('mine_stage.png', confidence=0.9)
            print("Stage end detected")
            break
        except pyautogui.ImageNotFoundException:
            pyautogui.press('p')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(3)
