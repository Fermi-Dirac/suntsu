import PIL
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import numpy as np
import os

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

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
numbers = Image.open(r'src_imgs\numbers only.png')#.convert('L')
npimg = np.array(numbers)
softmax = np.max(npimg)-(255*0.15)
softmin = np.min(npimg) + (255*0.15)
npimg[npimg>softmax] = 254
npimg[npimg<softmin] = 1
bwnumbs = Image.fromarray(npimg)
# bwnumbs.show()

# Simple image to string
for path in list_folder(r'src_imgs\numbers', fullpaths=True):
    print(f"From: {path}")
    # print(f"Default: {pytesseract.image_to_string(path)}")
    gray = Image.open(path).convert('L')
    # print(f"Gray: {pytesseract.image_to_string(gray)}")
    npimg = np.array(gray)
    softmax = np.max(npimg) - (255 * 0.15)
    softmin = np.min(npimg) + (255 * 0.15)
    npimg[npimg > softmax] = 254
    npimg[npimg < softmin] = 1
    npimg = 255 - npimg
    bwnumbs = Image.fromarray(npimg)
    print(f"BW Enhance: {pytesseract.image_to_string(bwnumbs)}")
    bwnumbs.resize((4*bwnumbs.width,4*bwnumbs.height),resample=PIL.Image.LANCZOS)
    bwnumbs.show()
    print(f"BW Big: {pytesseract.image_to_string(bwnumbs)}")

# column = Image.open('')
# gray = column.convert('L')
# blackwhite = gray#.point(lambda x: 0 if x < 150 else 255, '1')
# blackwhite.save("stats.jpg")m

def extract_text(img, validate=False):
    if type(img) is str:
        gray = Image.open(img).convert('L')
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
