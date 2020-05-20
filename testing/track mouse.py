#! python3
import time
import pyautogui, sys
print('Press Ctrl-C to quit.')
try:
    while True:
        time.sleep(0.1)
        x, y = pyautogui.position()
        print(f"({x:04d}, {y:04d})")
except KeyboardInterrupt:
    print('\n')