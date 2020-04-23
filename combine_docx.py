from docx import Document
import os
from win32com import client as wc

for i in os.listdir("files"):
    doc_all = Document()
    for j in os.listdir("files/" + i):
        filename, aff = os.path.splitext(j)
        if aff == ".doc":
            w = wc.DispatchEx('Word.Application')
            print("files/" + i + '/' + j)
            doc = w.Documents.Open("D:/exercises/files/" + i + '/' + j)
            doc.SaveAs("D:/exercises/files/" + i + '/' + filename + ".docx", 12)
            doc.Close()
            doc = Document("files/" + i + '/' + filename + ".docx")
        else:
            doc = Document("files/" + i + '/' + j)
        for para in doc.paragraphs:
            doc_all.add_paragraph(para.text)
    doc_all.save(i + '.docx')  # 保存文档
