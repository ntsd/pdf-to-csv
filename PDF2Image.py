# not done

import PyPDF2

from PIL import Image

import sys
from os import path

def recurse(page, xObject):

    xObject = xObject['/Resources']['/XObject'].getObject()

    for obj in xObject:

        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj]._data
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            imagename = "%s - p. %s - %s"%(abspath[:-4], p, obj[1:])

            print("page:"+str(page), "Decode:"+xObject[obj]['/Filter'], "color:",xObject[obj]['/ColorSpace'])

            if xObject[obj]['/Filter'] == '/FlateDecode':
                print(len(data), size)
                img = Image.frombytes(mode, size, data)
                img.save("tmp/"+imagename + ".png")
            elif xObject[obj]['/Filter'] == '/DCTDecode':
                img = open("tmp/"+imagename + ".jpg", "wb")
                img.write(data)
                img.close()
            elif xObject[obj]['/Filter'] == '/JPXDecode':
                img = open("tmp/"+imagename + ".jp2", "wb")
                img.write(data)
                img.close()
        else:
            recurse(page, xObject[obj])


if __name__ == "__main__":
    filename = "24072017105237.pdf"
    abspath = path.abspath(filename)

    file = PyPDF2.PdfFileReader(open(filename, "rb"), strict=False)

    for p in range(file.getNumPages()):
        page0 = file.getPage(p)
        recurse(p, page0)

    print('extracted images')