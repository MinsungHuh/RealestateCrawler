import xlsxwriter
import sqlite3

conn = sqlite3.connect("certified_realestate.db")
workbook = xlsxwriter.Workbook('전국_부동산중개업소_목록_20170828.xlsx')
worksheet = workbook.add_worksheet()
column_title = [
    "index",
    "등록번호",
    "시",
    "구군",
    "읍면동",
    "상호",
    "소재지",
    "대표자",
    "전화번호",
    "상태",
    "위도",
    "경도",
    "우편번호"
]

def get_realestate():
    query = "SELECT * FROM certified_realestate ORDER BY id ASC"
    cursor = conn.cursor()
    return cursor.execute(query).fetchall()


def export_excel():
    for index in range(0, 13):
        worksheet.write(0, index, column_title[index])
    rows = get_realestate()

    index = 1
    for row in rows:
        for column in range(0, 13):
            worksheet.write(index, column, row[column])
        index += 1

    workbook.close()


export_excel()
