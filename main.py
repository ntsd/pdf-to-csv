import ImageOCR
import PDF2Image
from Text2CSV import TextToCsv
import glob

if __name__ == "__main__":
    # PDF to Images
    pdf_path = "sample_pdf/24072017105237.pdf"  # path of pdf
    PDF2Image.pdf2image(pdf_path, "tmp/tmp.jpg")

    # Image to CSV
    image_paths = glob.glob("tmp/*.jpg")  # path of images
    text_to_csv = TextToCsv()
    text_to_csv.path = "output.csv"  # path to save in csv
    col = 7  # col to extract to csv
    for path in image_paths:
        print(path)
        im_out = ImageOCR.preprocess(path)
        text = ImageOCR.image_to_string(im_out)
        print(text)
        text_to_csv.extract_by_col(texts=text, column=col)
    # print(text_to_csv.csv_text_lists)
    text_to_csv.save()
