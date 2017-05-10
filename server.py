#!/Users/oucb/Program/python/tmap/venv/bin/python
# server.py

import json
import requests
from geojson import Point, Feature
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

ROUTE = [{"long": 104.163, "lat": 35.942, "name": "兰州", "have_been_to": False, "message": '兰大，榆中。。。寸草不生的荒凉山脊，一眼望去的白雪，豪爽的北方汉子，图书馆的遇见，太多的美好。208宿舍，翠英山，你们。。。'},
         {"long": 113.661, "lat": 34.747, "name": "郑州", "have_been_to":False, "message": '一伙老乡找的小餐馆，大家提着行旅逛公园，孩童般的新奇，想起一起爬的兴隆山，一起在农家乐聚会，一起吃的火锅，一起在本部等车'},
        {"long": 115.797, "lat": 25.600, "name": "赣州", "have_been_to": False, "message": '故乡，心中永远的热土。家乡，永远都是心中的最美'},
         {"long": 113.323, "lat": 23.133, "name": "广州", "have_been_to": False, "message": '一座文化、潮流之城，包容且一枝独秀'},
         {"long": 115.978, "lat": 29.571, "name": "九江", "have_been_to": False, "message": '庐山，八里湖，埋下许多记忆的种子。713遇见了很多前辈、同事，他们真好！江熠师父，像朋友、兄长！'},
         {"long": 108.379, "lat": 30.808, "name": "重庆", "have_been_to": False, "message": '永远的第一次烧仙草，校园路上听你道着你的大学时光。喜欢一个人时的欢喜，心里放着一个人的幸福，仿佛充满勇气与力量，真美好！'},
         {"long": 115.978, "lat": 29.571, "name": "九江", "have_been_to": True, "message": '庐山，八里湖，埋下许多记忆的种子。'},
         {"long": 117.992, "lat": 27.685, "name": "武夷山", "have_been_to": False, "message": '第一次旅行，所里组织的，九曲漂流好玩。'},
         {"long": 115.978, "lat": 29.571, "name": "九江", "have_been_to": True, "message": '庐山，八里湖，埋下许多记忆的种子'},
         {"long": 115.968, "lat": 39.482, "name": "涿州", "have_been_to": False, "message": '第一次出差，门卫处的大狼狗，看到了坦克，一位可以一起开心玩耍的前辈！'},
         {"long": 116.404, "lat": 39.913, "name": "北京", "have_been_to": False, "message": '第一次吃煎饼果子，念念不忘。我说没去过北京，前辈让我一个人在那玩一天再回公司，出差的东北阿姨叫我有机会去看松花江'},
         {"long": 119.446, "lat": 32.384, "name": "扬州", "have_been_to": False, "message": '一路押车，司机半夜叫醒我看金光闪闪的宝塔，您们真好！湖南会馆，瘦西湖，看电影、打电玩，还是那位开心玩耍的前辈'},
         {"long": 118.789, "lat": 32.020, "name": "南京", "have_been_to": False, "message": '第一次一个人出差，提着几十万的设备，一个人逛了夫子苗，瞻园，吃了鸭血粉丝'},
         {"long": 115.978, "lat": 29.571, "name": "九江", "have_been_to": True, "message": '庐山，八里湖，埋下许多记忆的种子'},
         {"long": 114.408, "lat": 30.503, "name": "武汉", "have_been_to": False, "message": '汇聚了这一行国内所有排得上号的研究所，认识了很多从事这一行业的伙伴，参与了很多，学到许多，谢谢几位前辈的关照！第一次见到那么多高级军官'},
         {"long": 120.842, "lat": 37.301, "name": "栖霞", "have_been_to": False, "message": '从武汉一路押车到大连，谢谢开车的黄师傅！栖霞吃了一顿饭，买了一箱超好吃的苹果。坐在车上看一路的风景'},
         {"long": 121.583, "lat": 38.881, "name": "大连", "have_been_to": False, "message": '一个月起早贪黑，天天在海边望风，各种海鱼、海鲜，认识他们真好！'},
         {"long": 117.188, "lat": 39.155, "name": "天津", "have_been_to": False, "message": '天津之眼，红旗饭庄，我们，老朋友'},
         {"long": 120.136, "lat": 30.263, "name": "杭州", "have_been_to": False, "message": '四位老朋友，我们在一起。。。'},
         {"long": 120.007, "lat": 26.888, "name": "霞浦", "have_been_to": False, "message": '遇见你们真好！北岐，美好的一天！做自己，不讨好'},
         {"long": 118.073, "lat": 24.455, "name": "厦门", "have_been_to": False, "message": '厦门，包容、注重细节的城市'},
         {"long": 114.056, "lat": 22.637, "name": "深圳", "have_been_to": False, "message": '深圳，一年半，一个人买菜、做饭、吃饭，coding、散步，遇见很多美好，书、音乐、电影'},
         {"long": 116.118, "lat": 30.154, "name": "宿松", "have_been_to": False, "message": '老朋友的婚礼，真好！'},
         {"long": 116.026, "lat": 28.682, "name": "南昌", "have_been_to": False, "message": '火车站等凌晨的火车，冻死。。。'}
         ]

ROUTE_URL = "https://api.mapbox.com/directions/v5/mapbox/driving/{0}.json?access_token={1}&overview=full&geometries=geojson"

def create_route_url():
    lat_longs = ";".join(["{0},{1}".format(point["long"], point["lat"]) for point in ROUTE])
    url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
    return url

def get_route_data():
    route_url = create_route_url()
    result = requests.get(route_url)
    data = result.json()
    geometry = data["routes"][0]["geometry"]
    route_data = Feature(geometry = geometry, properties = {})
    return route_data


def create_stop_locations_details():
    stop_locations = []
    locations_index = 0
    for route_index, location in enumerate(ROUTE):
        if location["have_been_to"]:
            continue
        locations_index = locations_index + 1
        point = Point([location['long'], location['lat']])
        properties = {
            'title': location['name'],
            'icon': 'campsite',
            'marker-color': '#3bb2d0',
            'marker-symbol': route_index,
            'route_index':route_index,
            'locations_index': locations_index,
            'msg':location['message']
        }
        feature = Feature(geometry=point, properties=properties)
        stop_locations.append(feature)
    return stop_locations


@app.route('/tmap')
def tmap():
    route_data = get_route_data()
    stop_locations = create_stop_locations_details()

    return render_template('tmap.html', ACCESS_KEY=MAPBOX_ACCESS_KEY,
                            route_data=route_data,
                            stop_locations=stop_locations
                            )

