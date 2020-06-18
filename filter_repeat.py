from docx import Document

fn = "一句话感言（编辑后）.docx"
doc = Document(fn)
count = 0
reg = []
repeat = []
for i in doc.paragraphs:
    count += 1
    if count % 2 == 0:
        if i.text[:2] != "——":
            print("error! " + i.text)
        else:
            if i.text[2:] in reg:
                if i.text[2:] not in repeat:
                    repeat.append(i.text[2:])
            else:
                reg.append(i.text[2:])
print(",".join(repeat))
