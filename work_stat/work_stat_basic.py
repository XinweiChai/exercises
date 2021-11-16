import openpyxl
from datetime import datetime

import easygui

# from tkinter import *
# from tkinter.filedialog import askopenfilename
# from tkinter.messagebox import showinfo

default_offset = 6


def work_statistics(fn, y_offset=default_offset, holidays=None):
    workbook = openpyxl.load_workbook(fn)
    sheet = workbook.worksheets[0]
    rows = (sheet.max_row - y_offset) // 2
    days = sheet.max_column
    for i in range(rows):
        absence_count = 0
        not_enough_count = 0
        absence = ""
        not_enough = ""
        for j in range(1, days + 1):
            if j in holidays:
                continue
            x = sheet.cell(i * 2 + y_offset, j).value
            # print(x)
            if not x or len(x) < 10:
                absence_count += 1
                absence += str(j) + ' '
                continue
            start = datetime.strptime(x[0:5], "%H:%M")
            end = datetime.strptime(x[-5:], "%H:%M")
            if (end - start).seconds < 3600:
                absence_count += 1
                absence += str(j) + ' '
            # elif (end - start).seconds < 9 * 3600 - 6 * 60:
            elif start > datetime.strptime('08:35', '%H:%M') or end < datetime.strptime('17:30', '%H:%M'):
                not_enough_count += 1
                not_enough += str(j) + ' '
        sheet.cell(i * 2 + y_offset, days + 1, absence_count)
        sheet.cell(i * 2 + y_offset, days + 2, absence)
        sheet.cell(i * 2 + y_offset, days + 3, not_enough_count)
        sheet.cell(i * 2 + y_offset, days + 4, not_enough)
    sheet.cell(1, days + 1, "缺打卡天数")
    sheet.cell(1, days + 2, "缺打卡日期")
    sheet.cell(1, days + 3, "上班时间不足天数")
    sheet.cell(1, days + 4, "上班时间不足日期")
    workbook.save("res.xlsx")


def openfile():
    # frameT = Tk()
    # frameT.geometry('500x100+400+200')
    # frameT.title('Select file')
    # frame = Frame(frameT)
    # frame.pack(padx=10, pady=10)
    # frame1 = Frame(frameT)
    # frame1.pack(padx=10, pady=10)
    # v = StringVar()
    # ent = Entry(frame, width=50, textvariable=v).pack(fill=X, side=LEFT)
    # # btn = Button(frame, width=20, text='Choose file', command=openpyxl.load_workbook).pack(fill=X, padx=10)
    # ext = Button(frame, width=10, text='Run', command=work_statistics).pack(fill=X, side=LEFT)
    # etb = Button(frame, width=10, text='Exit', command=frameT.quit()).pack(fill=Y, padx=10)
    # frameT.mainloop()
    # v.set('')
    # file_name = askopenfilename()
    # if file_name:
    #     v.set(file_name)
    offset = easygui.enterbox('Y-offset', default='6')
    holidays = easygui.enterbox('Holidays split by space', default='6 7 13 14 20 21 25 26 27')
    if holidays:
        holidays = set(map(int, holidays.split()))
    if offset and offset.isdigit():
        offset = int(offset) + 1
    else:
        offset = default_offset
    fn = easygui.fileopenbox()
    if fn and holidays:
        work_statistics(fn, offset, holidays)


if __name__ == "__main__":
    # work_statistics("考勤机原始考勤.xlsx")
    openfile()
