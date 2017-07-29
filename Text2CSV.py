import csv
import codecs


class TextToCsv:
    raw_texts = ""
    path = "output.csv"
    csv_text_lists = []

    def extract_by_col(self, texts=None, column=None):
        if texts is None:
            texts = self.raw_texts
        if column is None:
            column = self.get_max_col()
        for row in texts.split("\n"):
            cols = row.split()
            if len(cols) == column:
                self.csv_text_lists.append(cols)

    def save(self, path=None):
        if path is None:
            path = self.path
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in self.csv_text_lists:
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
