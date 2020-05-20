from suntsu import extract
import cv2
import numpy as np

num_guesses = dict()
for i in range(10):
    if i == 1:
        num_pixel_spacing = 9
    else:
        num_pixel_spacing = 20
    test_img_path = r'..\src_imgs\numbers\Long tests\1358880.png'
    alloc = extract.locate_numbers(test_img_path, i, num_pixel_spacing=num_pixel_spacing, show=False)
    print(alloc)
    num_guesses[i]=alloc

best_row = -10
all_rows = []
all_cols = []
col_width=5
for number, cand_list in num_guesses.items():
    for cand in cand_list:
        all_rows.append(cand[0])
        all_cols.append(cand[1])
all_cols.sort()
number_cols = []
last_col = all_cols[0]
occurances = 0
positional_candidates = dict()  # key is column, value is list of candidates from all numbers.
for col in all_cols:
    if last_col-col_width < col < last_col+col_width:
        occurances += 1
    else:
        print(f"Column {col} occured {occurances} times. Probably a number")
        occurances=0
        number_cols.append(col)
        last_col = col
        positional_candidates[col] = []  # Prep the dictionary to start looking here
best_row = np.median(all_rows)
for number_col in positional_candidates.keys():
    # Populate this entry with a list
    for number, cand_list in num_guesses.items():
        for cand in cand_list:
            if number_col - col_width < cand[1] < number_col + col_width:
                if cand[0]-3 < best_row < cand[0]+3:
                    positional_candidates[number_col].append((number, cand))
                else:
                    print(f"Bad row for {cand}")

for col, cand_list in positional_candidates.items():
    print(f"At col {col}")
    for number, cand in cand_list:
        print(f"\t{number}? :{cand[2]}")
