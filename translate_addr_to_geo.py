import sqlite3
import urllib

import requests

conn = sqlite3.connect("certified_realestate.db")


def get_realestate():
    query = "SELECT id, name, address FROM certified_realestate WHERE zip_code is NULL ORDER BY id"
    cursor = conn.cursor()
    return cursor.execute(query).fetchall()


def update_address(item):
    id = item['id']
    name = item['name']
    lat = item['lat']
    lng = item['lng']
    zip_code = item['zone_no']

    query = "UPDATE certified_realestate SET lat = ?, lng = ?, zip_code = ? WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, (lat, lng, zip_code, id))
    conn.commit()

    print('id: %s / name: %s / lat: %s / lng: %s updated!' % (id, name, lat, lng))


def translate_addr_to_geo():
    rows = get_realestate()

    for row in rows:
        id = row[0]
        name = row[1]
        address = urllib.parse.quote(row[2])

        url = "https://dapi.kakao.com/v2/local/search/address.json?query=%s" % address
        print('url', url)
        headers = {'Authorization': 'KakaoAK eea2d2fd1428b73cd2fe292d7bb962a5'}
        response = requests.get(url, headers=headers).json()

        if response['meta']['total_count'] <= 0:
            print('not converted.')
            continue

        item = response['documents'][0]['road_address']
        if item is None:
            item = response['documents'][0]['address']
            data = {
                "id": id,
                "name": name,
                "zone_no": item['zip_code'],
                "lat": item['y'],
                "lng": item['x']
            }
        else:
            data = {
                "id": id,
                "name": name,
                "zone_no": item['zone_no'],
                "lat": item['y'],
                "lng": item['x']
            }

        update_address(data)


def translate_addr_to_geo_by_naver():
    rows = get_realestate()
    for row in rows:
        id = row[0]
        name = row[1]
        enc_address = urllib.parse.quote(row[2])
        url = "https://openapi.naver.com/v1/map/geocode?query=%s" % enc_address
        header = {
            'X-Naver-Client-Id': 'Tehtk3IJTxiFGeHIek8e',
            'X-Naver-Client-Secret': 'Vk1RXAGEqL'
        }

        response = requests.get(url, headers=header).json()
        if response['result']['total'] <= 0:
            print('not converted.')
            continue

        lat = response['result']['items'][0]['point']['y']
        lng = response['result']['items'][0]['point']['x']
        data = {
            'id': id,
            'name': name,
            'zone_no': 'null',
            'lat': lat,
            'lng': lng
        }

        update_address(data)


translate_addr_to_geo()
