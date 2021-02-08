import io
from math import dist, cos
import sys
from PIL import Image
import requests


def get_distance(lat1, long1, lat2, long2):
    lat1 = 111 * cos(long1)
    lat2 = 111 * cos(long2)
    long1 *= 111
    long2 *= 111
    return dist((lat1, long1), (lat2, long2)) * 1000


def get_middle_point(address):
    payload = {
        "geocode": address,
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json"
    }
    resp = requests.get("http://geocode-maps.yandex.ru/1.x/", params=payload)
    if resp.ok:
        json_resp = resp.json()
        pos = json_resp["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["Point"]["pos"].replace(" ", ",")
        return pos


def get_closest_pharmacy(center):
    payload = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "ll": center,
        "lang": "ru_RU",
        "type": "biz"
    }
    resp = requests.get("https://search-maps.yandex.ru/v1/", params=payload)
    if resp.ok:
        return resp.json()["features"][0]["properties"]


def show_map(middle_pos, pharmacy_pos):
    payload = {
        "ll": middle_pos,
        "l": "map",
        "pt": f"{middle_pos},pm2dbm1~{pharmacy_pos},pm2rdm2"
    }
    # 1 - дом, 2 - аптека
    resp = requests.get("http://static-maps.yandex.ru/1.x/", params=payload)
    if resp.ok:
        Image.open(io.BytesIO(resp.content)).show()


def main():
    middle_pos = get_middle_point(" ".join(sys.argv[1:]))
    json_data = get_closest_pharmacy(middle_pos)
    pharmacy_pos = get_middle_point(json_data["CompanyMetaData"]["address"])
    distance = get_distance(*map(float, middle_pos.split(',')),
                            *map(float, pharmacy_pos.split(',')))
    print(json_data["CompanyMetaData"]["address"])
    print(json_data["name"])
    print(f"Расстояние = {distance:.3f}м")
    show_map(middle_pos, pharmacy_pos)


if __name__ == '__main__':
    main()
