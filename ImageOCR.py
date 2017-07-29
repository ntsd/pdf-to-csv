import difflib

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

import codecs

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


def check_diff(texts1, texts2): # use for check differ of 2 string
    print("\n---------check diff ----------")
    list_text1 = [i for i in texts1.split("\n")if i.strip() != ""]
    list_text2 = [i for i in texts2.split("\n")if i.strip() != ""]
    cases=zip(list_text1, list_text2)
    for text1,text2 in cases:
        print('old :{} \n------------------\nnew :{}'.format(text1, text2))
        # for i,s in enumerate(difflib.ndiff(text1, text2)):=
        #     if s[0]==' ': continue
        #     elif s[0]=='-':
        #         print(u'Delete "{}" from position {}'.format(s[-1],i))
        #     elif s[0]=='+':
        #         print(u'Add "{}" to position {}'.format(s[-1],i))
        print()
    return


def preprocess(url):
    im = Image.open(url)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1)
    #im = im.convert('1')
    im.save('tmp/temp.jpg')
    return im


def image_to_string(image):
    return pytesseract.image_to_string(image)

if __name__ == '__main__':
    im_out = preprocess('images/24072017105237-1.jpg')
    text = pytesseract.image_to_string(im_out)
    print(text)

    # use to check diff
    try:
        file = codecs.open('tmp/temp.text', 'r', "utf-8")
        old_text = file.read()
        check_diff(old_text, text)
        file = codecs.open('tmp/temp.text', 'w', "utf-8")
        file.write(text)
    except:
        file = codecs.open('tmp/temp.text', 'w', "utf-8")
        file.write(text)
    print("\n-------- END -----------")
