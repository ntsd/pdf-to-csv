import csv
import codecs


class TextToCsv:
    raw_texts = ""
    path = "output.csv"
    csv_text_lists = []
    col_range_start = 0
    col_range_end = 10

    def extract(self, texts=None):
        for row in texts.split("\n"):
            cols = row.split()
            self.csv_text_lists.append(cols)

    def extract_by_col(self, texts=None, column=None, col_range_start=None, col_range_end=None):
        if texts is None:
            texts = self.raw_texts
        if col_range_start and col_range_end:
            for row in texts.split("\n"):
                cols = row.split()
                if len(cols) in range(col_range_start, col_range_end+1):
                    self.csv_text_lists.append(cols)
        else:
            if column is None:
                column = self.get_max_col(texts)
            for row in texts.split("\n"):
                cols = row.split()
                if len(cols) == column:
                    self.csv_text_lists.append(cols)

    def filter_by_col_range(self, col_range_start=None, col_range_end=None, text_list=None):
        if text_list is None:
            text_list = self.csv_text_lists
        text_list_in_range = []
        for text_line in text_list:
            if len(text_line) in range(col_range_start, col_range_end+1):
                text_list_in_range.append(text_line)
        return text_list_in_range

    def save(self, path=None, text_lists=None):
        if path is None:
            path = self.path
        if text_lists is None:
            text_lists = self.csv_text_lists
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in text_lists:
                writer.writerow(row)

    def clear_list(self):
        self.csv_text_lists = []

    def get_max_col(self, texts=None):
        max_cols = 0
        if texts is None:
            texts = self.raw_texts
        for row in texts.split("\n"):
            cols = row.split()
            len_cols = len(cols)
            if len_cols > max_cols:
                max_cols = len_cols
        return max_cols

if __name__ == "__main__":
    text_to_csv = TextToCsv()
    file = codecs.open('temp.text', 'r', "utf-8")
    text_to_csv.raw_texts = file.read()
    text_to_csv.extract_by_col(7)
    print(text_to_csv.csv_text_lists)
    text_to_csv.save()
