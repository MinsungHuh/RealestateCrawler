import xlsxwriter
import sqlite3

conn = sqlite3.connect("certified_realestate.db")
workbook = xlsxwriter.Workbook('전국_부동산중개업소_목록_20170826.xlsx')
worksheet = workbook.add_worksheet()

def get_realestate():
    query = "SELECT * FROM certified_realestate ORDER BY id ASC LIMIT 100"
    cursor = conn.cursor()
    return cursor.execute(query).fetchall()


def export_excel():
    worksheet.write(0, 0, "index")
    worksheet.write(0, 1, "등록번호")
    worksheet.write(0, 2, "시")
    worksheet.write(0, 3, "구군")
    worksheet.write(0, 4, "읍면동")
    worksheet.write(0, 5, "상호")
    worksheet.write(0, 6, "소재지")
    worksheet.write(0, 7, "대표자")
    worksheet.write(0, 8, "전화번호")
    worksheet.write(0, 9, "상태")
    rows = get_realestate()

    index = 1
    for row in rows:
        for column in range(0, 10):
            worksheet.write(index, column, row[column])
        index += 1

    workbook.close()


export_excel()
