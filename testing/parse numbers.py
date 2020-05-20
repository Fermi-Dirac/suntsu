import cv2
import os
import numpy as np

def list_folder(rootpath : str, extensions = None, fullpaths=False, folders_only=False):
    """
    This function only lists the rootpath folder and its immediate contents
    :param rootpath:
    :param extensions:
    :return:
    """
    if not os.path.isdir(rootpath):
        rootpath = os.path.basename(rootpath)
    if extensions is None and folders_only is False:
        files = os.listdir(rootpath)
    else:
        if type(extensions) is not list:
            extensions = [extensions]
        if folders_only:
            files = [file for file in os.listdir(rootpath) if os.path.isdir(os.path.join(rootpath, file))]
        else:
            files = [file for file in os.listdir(rootpath) if any([file.endswith(ext) for ext in extensions])]
    if fullpaths:
        files = [rootpath + os.sep + file for file in files]
    return files

num_imgs = []
for path in list_folder('src_imgs/numbers', fullpaths=True, extensions='.png'):
    num_imgs.append(cv2.imread(path))

test1 = num_imgs[1]
template = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
tpl_height, tpl_width = template.shape[0:2]
cv2.imshow('template', template)
cv2.imshow('original', test1)
# cv2.waitKey()
resized = np.empty_like(test1)
parsed_nums = dict()
num_pixel_spacing = 5

# first, figure out which scale is best using a given number
def resize_to_best_scale(img2, num_scales=20, check_number=4, num_imgs=None):
    gray = cv2.cvtColor(img2, code=cv2.COLOR_BGR2GRAY)
    if num_imgs is None:
        num_imgs = []
        for path in list_folder('src_imgs/numbers', fullpaths=True, extensions='.png'):
            num_imgs.append(cv2.imread(path))
    resized = np.empty_like(img2)
    found = None
    num_img = num_imgs[check_number]
    resized_list = []
    for i, scale in enumerate(np.linspace(0.2, 1, num_scales)):
        print(f"Checking scale {scale}")
        resized = cv2.resize(gray, dst=resized, fx=1 / scale, fy=1 / scale, interpolation=cv2.INTER_NEAREST, dsize=None)
        ratio = gray.shape[1] / resized.shape[1]
        edgy = cv2.Canny(resized, 50, 200)
        match_result = cv2.matchTemplate(edgy, template, cv2.TM_CCOEFF_NORMED)
        _, maxval, _, maxloc = cv2.minMaxLoc(match_result)
        if found is None or maxval > found[0]:
            found = (maxval, match_result, ratio, scale, resized)
    return found[4]

# Now use that scale to check for all the other numbers

# Checking
for number, spots in parsed_nums.items():
    print(f"{number} at {spots}")


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


for img_path in list_folder(r'src_imgs/numbers/Long tests', extensions='.png', fullpaths=True):
    print(f"Now on {img_path}")
    img = cv2.imread(img_path)
    # gray = cv2.cvtColor(img, code=cv2.COLOR_BGR2GRAY)
    # found = None
    number_seq_img = img # resize_to_best_scale(img)
    parsed_nums = dict()
    for num_i, num_img in enumerate(num_imgs):
        print(f"Now checking for occurances of {num_i}")
        template = cv2.cvtColor(num_img, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        tpl_height, tpl_width = template.shape[0:2]

        parsed_nums[num_i] = []

        edgy = cv2.Canny(number_seq_img, 50, 200)
        match_result = cv2.matchTemplate(edgy, template, cv2.TM_CCOEFF_NORMED)
        softmax = 0.48
        locs = np.where(match_result > softmax) # Tuple of lists, list1, all of the rows, list2 all of the columns
        rows, cols = locs
        sorted_i = np.argsort(cols)
        rows = rows[sorted_i]
        cols = cols[sorted_i]
        # we just want unique columns with at least N pixels between them. So
        last_col = -1
        for i, col in enumerate(cols):
            if col > num_pixel_spacing//2 + last_col:
                parsed_nums[num_i].append((rows[i], col, match_result[rows[i], col]))
            last_col = col
        print(f"We found {len(parsed_nums[num_i])} different pictures of the digit {num_i}")
        # match_result[match_result < softmax] = 0


    output = candidate_number_to_final(parsed_nums)
    print(output)