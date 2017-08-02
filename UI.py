from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
import tkinter.scrolledtext as tkst

import ImageOCR
import PDF2Image
from Text2CSV import TextToCsv
import glob

import os


class MyFrame(Frame):
    filePath = ""
    image_paths = []
    col_to_extract = 7
    col_range_start = 0
    col_range_end = 10
    text_lists_to_out = []
    loaded = 0

    def __init__(self):
        Frame.__init__(self)
        self.master.title("PDF To CSV")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        self.browse_button = Button(self, text="Browse", command=self.load_file, width=10)
        self.browse_button.grid(row=0, column=0, sticky=W)

        self.directory_button = Button(self, text="Export to", command=self.set_out_folder, width=10)
        self.directory_button.grid(row=0, column=4, sticky=W)

        self.convert_button = Button(self, text="Export", command=self.Export, width=10)
        self.convert_button.grid(row=0, column=5, sticky=E)

        self.columnLabel = Label(self, text="Column to extract range:", width=20)
        self.columnLabel.grid(row=1, column=0, columnspan=2, sticky=W)

        self.start_range = StringVar(self)
        self.start_range.set("7")
        self.start_range.trace('w', self.filterColumn)
        self.columnSpinBoxStart = Spinbox(self, from_=1, to=20, width=4, textvariable=self.start_range)
        self.columnSpinBoxStart.grid(row=1, column=2, sticky=W)

        self.columnLabel = Label(self, text="to:", width=2)
        self.columnLabel.grid(row=1, column=3, sticky=W)

        self.end_range = StringVar(self)
        self.end_range.set("7")
        self.end_range.trace('w', self.filterColumn)
        self.columnSpinBoxEnd = Spinbox(self, from_=1, to=20, width=4, textvariable=self.end_range)
        self.columnSpinBoxEnd.grid(row=1, column=4, sticky=W)

        self.example_rows = Label(self, text="rows:0", width=4)
        self.example_rows.grid(row=1, column=5, sticky=W)

        self.example_output = tkst.ScrolledText(master = self,
                                                wrap   = WORD,
                                                width  = 60,
                                                height = 30)
        self.example_output.grid(row=2, column=0, columnspan=6, sticky=E)

        # self.imageLabel = Label(self, width=25, heigh=25) # 280/198
        # self.imageLabel.grid(row=2, column=0, columnspan=2, sticky=E+W)



        # TextToImage
        self.text_to_csv = TextToCsv()
        self.text_to_csv.path = "output.csv"

    def load_file(self):
        fname = askopenfilename(filetypes=(("PDF files", "*.pdf"),
                                           ("Image files", "*.jpg;*.png"),
                                           ("All files", "*.*")), initialdir = os.getcwd())
        if fname:
            try:
                self.filePath = fname
                self.pdfToImage()
                self.text_to_csv.clear_list()
                self.text_lists_to_out = []
                self.convert()
                print("""Load PDF Finish""")
                self.loaded = 1
                self.filterColumn()
            except:
                showerror("Open File", "Failed to read file\n'%s'" % fname)
            return

    def set_out_folder(self):
        dirname = askdirectory(initialdir=os.getcwd(),title='Please select a Directory')
        self.text_to_csv.path = dirname+"/output.csv"
        print("set out put path to :"+self.text_to_csv.path)

    def pdfToImage(self):
        PDF2Image.pdf2image(self.filePath, "tmp/tmp.jpg")
        self.image_paths = glob.glob("tmp/*.jpg")

    def convert(self):
        self.col_to_extract = int(self.columnSpinBoxStart.get())
        for path in self.image_paths:
            print("extracting : "+path)
            im_out = ImageOCR.preprocess(path)
            # self.showTmpImage(im_out)
            text = ImageOCR.image_to_string(im_out)
            self.text_to_csv.extract(texts=text)

        print("Convert Success")
        print("Removing Temp...")
        for path in self.image_paths:
            os.remove(path)
        print("Removing Temp Success")

    def filterColumn(self, name=None, index=None, mode=None):
        if self.loaded:
            print("Filter with column : "+self.columnSpinBoxStart.get()+" to "+self.columnSpinBoxEnd.get())
            self.text_lists_to_out = self.text_to_csv.filter_by_col_range(col_range_start=int(self.columnSpinBoxStart.get()),
                                                                          col_range_end=int(self.columnSpinBoxEnd.get()))
            self.example_output.delete('1.0', END) # clear text and replace
            text_example = ""
            for row in self.text_lists_to_out:
                text_example += ",".join(i for i in row)
                text_example += "\n"
            self.example_output.insert(INSERT, text_example)

            self.example_rows.text = "rows:"+str(len(self.text_lists_to_out))
        # print("Changed Column Range")
        self.start_range.get()


    def Export(self):
        self.text_to_csv.save(text_lists=self.text_lists_to_out)
        print("Saved output to :"+self.text_to_csv.path)

    def showTmpImage(self, img):
        self.imageLabel.image = img

if __name__ == "__main__":
    MyFrame().mainloop()
