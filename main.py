import ImageOCR
from Text2CSV import TextToCsv
import glob

if __name__ == "__main__":
    image_paths = glob.glob("images/*.jpg")  # path of images
    text_to_csv = TextToCsv()
    text_to_csv.path = "output.csv"  # path to save in csv
    for path in image_paths:
        im_out = ImageOCR.preprocess(path)
        text = ImageOCR.image_to_string(im_out)
        text_to_csv.extract_by_col(texts=text, column=text_to_csv.get_max_col())
    text_to_csv.save()
