import PyPDF2
import shutil
import os
import re

# directory = 'C:/Users/zby11/Desktop/test'
directory = 'C:/Users/Administrator/Desktop'


def rename_pdf(path):
    for file in os.listdir(path):
        (short_name, extension) = os.path.splitext(file)
        if extension == '.pdf':
            with open(os.path.join(path, file), 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                paper_title = pdf_reader.getDocumentInfo().title
                title = re.sub("[:?\"]", ",", str(paper_title))
            shutil.move(os.path.join(path, file), os.path.join(path, title + ".pdf"))


if __name__ == '__main__':
    rename_pdf(directory)
