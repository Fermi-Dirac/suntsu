import pyautogui as pg
import PIL
import time
print(pg.size())
img = pg.screenshot()
corner1 = pg.locateOnScreen(r'src_imgs/war/blue corner.png', confidence=0.9, grayscale=True)
number = [75, None, 120, 100]
number[1] = corner1[1]+10
# for loc in num1:
    # pg.click(loc, interval=1)
num_img = pg.screenshot(region=number)
# num_img.show()
scrollbar_loc = pg.locateOnScreen(r'src_imgs/war/scrollbar.png', grayscale=True, confidence=0.9)
pg.click(scrollbar_loc, interval=0.5)
for i in range(10):
    scrollbar_loc = pg.locateOnScreen(r'src_imgs/war/scrollbar.png', grayscale=True, confidence=0.9)
    pg.click(scrollbar_loc, interval=0.5)
    pg.dragRel(0, 44, 0.5)