import openpyxl
from datetime import datetime

holiday = [6, 7, 13, 14, 20, 21, 25, 26, 27]

y_offset = 5


def work_statistics(fn):
    workbook = openpyxl.load_workbook(fn)
    sheet = workbook.worksheets[0]
    rows = (sheet.max_row - y_offset) // 2 + 1
    days = sheet.max_column
    for i in range(rows):
        absence_count = 0
        not_enough_count = 0
        absence = ""
        not_enough = ""
        for j in range(1, days + 1):
            if j in holiday:
                continue
            x = sheet.cell(i * 2 + y_offset, j).value
            print(x)
            if not x or len(x) < 10:
                absence_count += 1
                absence += str(j) + ' '
                continue
            start = datetime.strptime(x[0:5], "%H:%M")
            end = datetime.strptime(x[-5:], "%H:%M")
            if (end - start).seconds < 3600:
                absence_count += 1
                absence += str(j) + ' '
            elif (end - start).seconds < 9 * 3600 - 6 * 60:
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


if __name__ == "__main__":
    work_statistics("考勤机原始考勤.xlsx")
