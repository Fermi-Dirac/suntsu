import cv2
import numpy as np
import os
from suntsu import setup_logger, module_path
logger = setup_logger(__name__)


def gray_it(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def black_white(img, threshold=20):
    ret = np.empty_like(img)
    ret[img>threshold] = img[img>threshold]
    ret[img<=threshold] = 0
    return ret


def corners(img, threshold1=50, threshold2=200):
    return cv2.Canny(img, threshold1, threshold2)


def candidate_number_to_final(parsed_nums, num_pixel_spacing=5):
    # Now we have our dictionary, we need to fix some mis-matches.
    # first we find the number of digits via number of quasi-unique columns
    pixel_cols = []
    checklist = []
    for number, spots in parsed_nums.items():
        for row, col, score in spots:
            if col not in checklist: # within num_pixel_spacing you are unique
                pixel_cols.append(col)
                checklist.extend(list(np.arange(col-num_pixel_spacing, col+num_pixel_spacing)))
    pixel_cols.sort()
    print(pixel_cols)
    # Now we see for overlapping
    best_scores = [-1 for _ in pixel_cols]
    output_num_sequence = [-1 for _ in pixel_cols]
    for num_index, near_col in enumerate(pixel_cols):
        print(f"Checking for best number at index {num_index}")
        for number, spots in parsed_nums.items():
            for row, col, score in spots:
                if col == near_col or col in list(np.arange(near_col-num_pixel_spacing, near_col+num_pixel_spacing)):
                    #Then this number competes for this spot
                    if score > best_scores[num_index]:
                        # You win!
                        print(f"at index {num_index}, {number} fits better than {output_num_sequence[num_index]} because {score} > {best_scores[num_index]}")
                        best_scores[num_index] = score
                        output_num_sequence[num_index] = number
                    else:
                        pass # You lose, someone is better fit here
                else:
                    pass  # You're not competing for this spot
        print(f"Best match was {output_num_sequence[num_index]} here.")
    return output_num_sequence


def locate_numbers(img, number=0, preproc=True, softmax=0.4, num_pixel_spacing=20, show=False):
    if type(img) is str:
        img = cv2.imread(img)
        if img is None:
            raise TypeError(f"Unknown image: {img} of type {type(img)}")
    num_img = cv2.imread(os.path.join(module_path,'src_imgs','numbers',f'{number}.png'))
    proc_img = black_white(gray_it(img))
    template = black_white(gray_it(num_img))
    tpl_height, tpl_width = template.shape[0:2]
    # now we look
    match_result = cv2.matchTemplate(proc_img, template, cv2.TM_CCOEFF_NORMED, mask=None)
    locs = np.where(match_result > softmax)  # Tuple of lists, list1, all of the rows, list2 all of the columns
    rows, cols = locs
    sorted_i = np.argsort(cols)
    rows = rows[sorted_i]
    cols = cols[sorted_i]
    # we just want unique columns with at least N pixels between them. So
    last_col = None
    last_candidates = []
    all_occurances = []
    if show:
        cv2.imshow('original', num_img)
        cv2.imshow('template', template)
        cv2.imshow('target', img)
    for i, col in enumerate(cols):
        candidate = rows[i], col, match_result[rows[i], col]
        if i == 0:
            last_candidates = [candidate]
            last_col = col
            continue
        if col < num_pixel_spacing // 2 + last_col:
            # Add to the list of candidates in this area
            last_candidates.append(candidate)
        else:
            # Then we have a new set of candidates. Find the best, then make a new list
            last_candidates.sort(key=lambda cand: cand[2])
            best = last_candidates[-1]
            if show:
                cv2.imshow(f'{number}? @cl {best[1]}, pt={best[2]:.2f}',
                       img[best[0]:best[0] + tpl_height, best[1]:best[1] + tpl_width])
            all_occurances.append(best)
            # reset array
            last_candidates = [candidate]
        last_col = col
    logger.info(f"We found {len(all_occurances)} different pictures of the digit {number}")
    return all_occurances


if __name__ == '__main__':
    num_pixel_spacing = 9
    test_img_path = r'src_imgs\numbers\Long tests\1173214.png'
    num_path = r'src_imgs\numbers\3.png'

    alloc = locate_numbers(test_img_path, 1, num_pixel_spacing=7, show=True)
    print(alloc)
    cv2.waitKey()
