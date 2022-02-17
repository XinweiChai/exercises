import PyPDF2
import shutil
import os
import re
import sys


def rename_pdf(path):
    for file in os.listdir(path):
        (short_name, extension) = os.path.splitext(file)
        if extension == '.pdf':
            with open(os.path.join(path, file), 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f, strict=False)
                paper_title = pdf_reader.getDocumentInfo().title
                title = re.sub("[:?\"]", ",", str(paper_title))
            if paper_title and paper_title != 'untitled':
                x = pdf_reader.getPage(0)
                shutil.move(os.path.join(path, file), os.path.join(path, title + ".pdf"))


def modify_metadata(fn, title):
    with open(fn, 'rb') as fin:
        reader = PyPDF2.PdfFileReader(fin)
        writer = PyPDF2.PdfFileWriter()
        writer.appendPagesFromReader(reader)
        metadata = reader.getDocumentInfo()
        writer.addMetadata(metadata)
        # Write your custom metadata here:
        writer.addMetadata({
            '/Title': title
        })

        with open('result.pdf', 'wb') as fout:
            writer.write(fout)


def remove_image(fn):
    with open(fn, "rb") as inputStream:
        src = PyPDF2.PdfFileReader(inputStream)
        with open("dst.pdf", "wb") as outputStream:
            output = PyPDF2.PdfFileWriter()
            [output.addPage(src.getPage(i)) for i in range(src.getNumPages())]
            output.removeImages()
            output.write(outputStream)


if __name__ == '__main__':
    # directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    # f2 = "Spatio-temporal Clustering and Forecasting Method for Free-Floating Bike Sharing Systems"
    # modify_metadata('123.pdf', f2)
    # rename_pdf(directory)
    # rename_pdf('.')
    remove_image("TEF-Canada-Expression-Orale-150-Topics.pdf")
