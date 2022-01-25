import os  # 用于获取目标文件所在路径
from win32com import client as wc  # 导入模块

word = wc.Dispatch("kwps.application")  # 打开wps应用程序

path = os.getcwd() + '/'
for file in os.listdir("."):
    # (file_path, temp_file_name) = os.path.split(file)
    (short_name, extension) = os.path.splitext(file)
    print(short_name)
    if extension == '.docx':
        doc = word.Documents.Open(path + file)
        doc.SaveAs(path + short_name + ".doc", 0)  # 另存为后缀为".doc"的文件，其中参数0指doc文件
        doc.Close()
word.Quit()