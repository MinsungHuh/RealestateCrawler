import requests
import sqlite3

# SQLite DB 연결
conn = sqlite3.connect("certified_realestate.db")

sigungu_url = "http://www.nsdi.go.kr/zcms/nsdi/land/searchSigungu.html"
dong_url = "http://www.nsdi.go.kr/zcms/nsdi/land/searchDong.html"
SIDO = {
    11: '서울특별시',
    26: '부산광역시',
    27: '대구광역시',
    28: '인천광역시',
    29: '광주광역시',
    30: '대전광역시',
    31: '울산광역시',
    36: '세종특별자치시',
    41: '경기도',
    42: '강원도',
    43: '충청북도',
    44: '충청남도',
    45: '전라북도',
    46: '전라남도',
    47: '경상북도',
    48: '경상남도',
    50: '제주특별자치도',
}


def search_realestate():
    for sido in SIDO: # 부산광역시

        sigungu_json = requests.post(sigungu_url, {'sido': sido}).json()['sigunguList']
        for sigungu in sigungu_json:
            gugun_code = sigungu['sggCd']
            gugun_name = sigungu['sggNm'] # 금정구

            dong_json = requests.post(dong_url, {'sigungu': gugun_code}).json()['dongList']
            for dong in dong_json:
                dong_code = dong['lawdCd']
                dong_name = dong['umdNm']

                flag = True
                page_index = 1
                while flag:
                    url = "http://www.nsdi.go.kr/?menuno=2776&pageIndex=%d" % page_index
                    data = {
                        'shInit': 'N',
                        'pageIndex': 1,
                        'shSido': sido,
                        'shSigungu': gugun_code,
                        'shDong': dong_code,
                        'shSelect': '1',
                        'shSelect2': '1',
                        'shCondi': '',
                        'shSelect3': '01',
                        'shWord': '',
                        'orderSelect': '00'
                    }

                    response = requests.post(url, data).text
                    response = response.split("<tbody>")[2].split("</tbody>")[0].split("<tr>")
                    response.pop(0)

                    print('city: ' + SIDO.get(sido))
                    print('district: ' + gugun_name)
                    print('neighborhood: ' + dong_name)

                    if "기록이 없습니다." in response[0]:
                        flag = False
                        print('pageIndex: %d not exist and continued' % page_index)
                        continue

                    index = 0
                    for value in response:
                        register_number = get_register_number(value)
                        name = get_realestate_name(value)
                        address = get_realestate_address(value)
                        owner_name = get_realestate_owner_name(value)
                        number = get_realestate_number(value)
                        operating_type = get_realestate_operating_type(value)

                        item = {
                            'sido': SIDO.get(sido),
                            'gugun': gugun_name,
                            'dong': dong_name,
                            'register_number': register_number,
                            'name': name,
                            'address': address,
                            'owner_name': owner_name,
                            'number': number,
                            'operating_type': operating_type
                        }
                        insert_realestate_data(item)

                        index += 1
                    page_index += 1


def validate_form(item):
    if '기록이 없습니다.' in item:
        print('기록이 없대요!')
        return False


def get_register_number(item):
    return item.split('<td class="t_c">')[2].split('</td>')[0].strip()


def get_realestate_name(item):
    return item.split('<a href="#">')[1].split('</a>')[0].strip()


def get_realestate_address(item):
    return item.split('<td alt="')[1].split('"')[0].strip()


def get_realestate_owner_name(item):
    return item.split('<td class="t_c">')[3].split('</td>')[0].strip()


def get_realestate_number(item):
    return item.split('<td class="t_c" alt="')[1].split('"')[0].strip()


def get_realestate_operating_type(item):
    return item.split('<td title="')[1].split('">')[0].strip()


def insert_realestate_data(item):
    sido = item['sido']
    gugun = item['gugun']
    dong = item['dong']
    register_number = item['register_number']
    name = item['name']
    address = item['address']
    owner_name = item['owner_name']
    number = item['number']
    operating_type = item['operating_type']

    cursor = conn.cursor()
    query = "INSERT INTO certified_realestate (register_code, city, district, neighborhood, name, address, owner_name, phone_number, operation_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (register_number, sido, gugun, dong, name, address, owner_name, number, operating_type))
    conn.commit()

    print('name: ' + name + " inserted")

# search_realestate()
