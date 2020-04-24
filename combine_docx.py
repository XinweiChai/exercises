from docx import Document
import os
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from win32com import client as wc
from docx.oxml.ns import qn

path = os.getcwd()
for i in os.listdir("files"):
    doc_all = Document()
    doc_all.styles['Normal'].font.size = Pt(10.5)
    doc_all.styles['Normal'].font.name = u'仿宋_GB2312'
    doc_all.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋_GB2312')
    for j in os.listdir("files/" + i):
        filename, aff = os.path.splitext(j)
        if aff == ".doc":
            w = wc.DispatchEx('Word.Application')
            doc = w.Documents.Open(path + "/files/" + i + '/' + j)
            doc.SaveAs(path + "/files/" + i + '/' + filename + ".docx", 12)
            doc.Close()
            continue
        else:
            doc = Document("files/" + i + '/' + j)
        print("files/" + i + '/' + j)
        count = 0
        for para in doc.paragraphs:
            if len(para.text) == 0 or para.text.isspace():
                continue
            count += 1
            if count == 1:
                paragraph = doc_all.add_paragraph()
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                run = paragraph.add_run(para.text.replace(" ", ""))
                run.font.name = u'方正小标宋简体'
                run.font.size = Pt(16)
                run._element.rPr.rFonts.set(qn('w:eastAsia'), u'方正小标宋简体')
            elif count == 2 or count == 3:
                paragraph = doc_all.add_paragraph()
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                run = paragraph.add_run(para.text.replace(" ", ""))
                run.font.name = u'楷体'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), u'楷体')
            else:
                doc_all.add_paragraph(para.text.strip())
    doc_all.save(i + '.docx')
