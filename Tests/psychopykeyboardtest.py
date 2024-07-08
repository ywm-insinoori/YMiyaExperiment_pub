from psychopy.hardware.keyboard import Keyboard
from psychopy import core

kb = Keyboard()

ctr = 0

while True:
    core.wait(0.1)
    ctr += 1
    keys = kb.getKeys() 
    for k in keys:
        print(k.name)
    if ctr > 200:
        print("Timed out")
        break
    if "space" in keys:
        print("Space pressed and detected by PsychoPy")
        break