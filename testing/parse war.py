import PIL
from PIL import Image
import pytesseract
import numpy as np
import os

import pyautogui as pg
import time
from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# box is [left, top, width, height]
locations = {'war participation': {'toggle' : [100, 200],
                                   'top player': [100, 340],
                                   'name+head': [190, None,340,60],
                                   'name': [280,None,350,60],
                                   'bottom player': (100, 340+138*4),
                                   'player spacing' :138,
                                   'text spacing' : 60,
                                   'stats': (1075, 175),
                                   'tcp': (1520,285,150,60),  # left, top, width, height
                                   'stp':(1520, 285+60, 150, 60),
                                   'top bar':280,
                                   'drag windup':35,
                                   'number': [75, None, 110, 70],
                                   'players list': [50, 250, 600, 600 ],
                                   }}
warloc = locations['war participation']

def extract_text(img, validate=False):
    if type(img) is str:
        gray = PIL.Image.open(img).convert('L')
    else:
        gray = img.convert('L')
    npimg = np.array(gray)
    softmax = np.max(npimg) - (255 * 0.15)
    softmin = np.min(npimg) + (255 * 0.15)
    npimg[npimg > softmax] = 254
    npimg[npimg < softmin] = 1
    npimg = 255 - npimg
    bwnumbs = Image.fromarray(npimg)
    text = pytesseract.image_to_string(bwnumbs)
    if validate == 'numbers':
        text = int(text)
    return text


def kill_ad(force=True):
    close_loc = pg.locateOnScreen(r'src_imgs/redX.png', confidence=0.8)
    if close_loc is None:
        print("No red X found!")
    if close_loc is not None:
        pg.click(close_loc, interval=0.5)
    elif force:
        pg.click((1480,216), interval=0.5)
    else:
        print("Couldn't find the ad.")


def toggle_war_opponents():
    for _ in range(5):
        toggle_loc = pg.locateOnScreen(r'src_imgs/war toggle opponents.png')
        if toggle_loc is None:
            pg.click(warloc['toggle'], interval=0.7)
        else:
            print("Opponents shown!")
            return True
    print("Couldn't get opponents only to work")
    return False


def extract_player_data(save_imgs=False, sanity=True):
    # loc = warloc['top player'][0], warloc['top player'][1] + pos * warloc['player spacing']
    # pg.click(loc, interval=interval)
    # pg.click(warloc['stats'], interval=interval)
    # name_loc = warloc['top name'].copy()
    # name_img = pg.screenshot(region=name_loc)
    # name_img.show()
    # name = extract_text(name_img)
    tcp_img = pg.screenshot(region=warloc['tcp'])
    tcp = extract_text(tcp_img)
    stp_img = pg.screenshot(region=warloc['stp'])
    stp = extract_text(stp_img)
    vals = [tcp, stp]
    imgs = tcp_img, stp_img
    if sanity:
        for i, val in enumerate(vals):
            if not val.isdecimal():
                # print(f"{val} is not a decimal")
                val = val.strip()
                for repl in r']|[()\/':
                    val = val.replace(repl, '1')
            try:
                vals[i] = int(val)
            except ValueError:
                print(f"Can't figure our parsed text: {val}")
                imgs[i].show()
                vals[i] = np.nan
        tcp, stp = vals
        if tcp > 7E6:
            print("TCP greater than 7 million!")
            tcp = tcp //10
        if stp > tcp:
            print("Error, STP > TCP! shifting by 10x")
            stp = stp//10
    data = {'tcp': tcp, 'stp': stp}
    if save_imgs:
        return data, imgs
    else:
        return data


def scroll_to_next_five():
    for _ in range (5):
        scroll_one_player()
    # pg.scroll(-2, pause=True)
    # loc = warloc['top player'][0], warloc['top player'][1] + 2 * warloc['player spacing']
    # pg.click(loc, interval=0.5)
    # pg.drag(0, -warloc['player spacing']*1-warloc['drag windup'], 5, button='left')
    # pg.click(duration=1)
    # _, newtop = pg.position()
    # return newtop


def scroll_one_player():
    scrollbar_loc = pg.locateOnScreen(r'src_imgs/war/scrollbar.png', grayscale=True, confidence=0.9)
    pg.click(scrollbar_loc, interval=0.5)
    pg.dragRel(0, 40, 0.5)
    #
    # loc = warloc['top player'][0], warloc['top player'][1] + 2 * warloc['player spacing']
    # pg.click(loc, interval=0.5)
    # pg.drag(0, -warloc['player spacing']*1-warloc['drag windup'], 5, button='left')


def find_shown_war_players(get_names=True):
    first_corner = pg.locateOnScreen(r'src_imgs/war/blue corner.png', confidence=0.9)
    number_loc = warloc['number'].copy()
    number_loc[1] = first_corner[1]+10
    print(pg.size())
    num_img = pg.screenshot(region=number_loc)
    num_img.show()
    for i in range(3):
        if number_loc:
            pass
    return all_locs, all_names


def find_top_war_player(index=0):
    first_corner = pg.locateOnScreen(r'src_imgs/war/red corner.png', region=warloc['players list'], confidence=0.9, grayscale=True)
    # if first_corner[1] > 240:
    #     # Wrong spot!
    #     all_corners = pg.locateAllOnScreen(r'src_imgs/war/red corner.png', confidence=0.9, grayscale=True)
    #     for corner in all_corners:
    #         if corner[1] > 240:
    #             first_corner = corner
    #             print("Searched for the next corner")
    #             break
    # number_loc = warloc['number'].copy()
    # number_loc[1] = first_corner[1]+15
    # num_img = pg.screenshot(region=number_loc)
    # num_img.show()
    name_loc = warloc['name'].copy()
    name_loc[1] = first_corner[1]+15
    # name_img = pg.screenshot(region=name_loc)
    # name_img.show()
    return name_loc

# for _ in range(5):
#     scroll_to_next_five()
#     print(pg.locateOnScreen('src_imgs/war corner.png'))
#     time.sleep(0.2)

#get opponent data only
toggle_war_opponents()
parsed_players = []
all_data = dict()
#1st player
nameloc = warloc['name'].copy()
nameloc[1] = 285
pg.click(nameloc, interval=0.5)
name_img = pg.screenshot(region=nameloc)
name = extract_text(name_img)
data = extract_player_data()
all_data[name] = data
parsed_players.append(name)
print(name, data)
# The Rest
for i in range(24):
    name_loc = find_top_war_player()
    name = extract_text(pg.screenshot(region=name_loc))
    print(f"Now extracting data for {name}")
    if name not in parsed_players:
        parsed_players.append(name)
        pg.click(name_loc, interval=0.5)
        data = extract_player_data()
        all_data[name] = data
    kill_ad()
    scroll_one_player()
print(all_data)
total_tcp = np.nansum([data['tcp'] for name, data in all_data.items()])
for name, data in all_data.items():
    print(f"{name} has tcp={data['tcp']}, stp={data['stp']}")
print(f"Total alliance power is {total_tcp}")


# all_data = {}
# for i in range(max):
#     if i < max-5:
#         name, data = extract_player_data(1)
#     else:
#         name, data = extract_player_data(max-i)
#     all_data[name] = data
#     print(f"{name} = {data}")
#     scroll_one_player()
# print(all_data)
# hist_data = [datum['tcp'] for name, datum in all_data.items()]
# plt.hist(hist_data)
# plt.show()