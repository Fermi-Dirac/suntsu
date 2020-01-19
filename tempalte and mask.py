import cv2
import numpy as np
import sys

# if len(sys.argv) < 3:
#     print ('Usage: python match.py <template.png> <image.png>')
#     sys.exit()

template_path = r'src_imgs\numbers\0.png'
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
channels = cv2.split(template)
zero_channel = np.zeros_like(channels[0])
mask = channels[0].copy()
mask[mask>50] = 255
mask[mask<50] = 0

image_path = r'src_imgs\numbers\Long tests\1358880.png'# sys.argv[2]
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# mask[channels[3] == 0] = 1
# mask[channels[3] == 100] = 0

# transparent_mask = None
# According to http://www.devsplanet.com/question/35658323, we can only use
# cv2.TM_SQDIFF or cv2.TM_CCORR_NORMED
# All methods can be seen here:
# http://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html#which-are-the-matching-methods-available-in-opencv
method = cv2.TM_SQDIFF  # R(x,y) = \sum _{x',y'} (T(x',y')-I(x+x',y+y'))^2 (essentially, sum of squared differences)

transparent_mask = mask # cv2.merge([zero_channel, zero_channel, zero_channel, mask])
print(image.shape, template.shape, method, transparent_mask.shape)
result = cv2.matchTemplate(image, template, method, mask=transparent_mask)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print ('Lowest squared difference WITH mask', min_val)

# Now we'll try it without the mask (should give a much larger error)
transparent_mask = None

result = cv2.matchTemplate(image, template, method, mask=transparent_mask)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print( 'Lowest squared difference WITHOUT mask', min_val)