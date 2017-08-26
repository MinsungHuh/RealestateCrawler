import sqlite3
import requests

conn = sqlite3.connect("certified_realestate.db")

def get_realestate():
    query = "SELECT id, name, address FROM certified_realestate ORDER BY id ASC LIMIT 100"
    cursor = conn.cursor()
    return cursor.execute(query).fetchall()


def translate_addr_to_geo():
    rows = get_realestate()
    for row in rows:
        id = row[0]
        name = row[1]
        address = row[2]

    url = "https://dapi.kakao.com/v2/local/search/address.json&query=%s"
    headers = {'Authorization': 'KakaoAK eea2d2fd1428b73cd2fe292d7bb962a5'}

    requests.get(url, headers)