import requests
import re
from bs4 import BeautifulSoup


print("ボートレースのURLを入力してください || ", end="")
url = input()


print("\n注意！! このデータを活用しようとする場合は、進入が変わるとデータが不正確になります。")

def id_from(url): 

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    return soup.find_all('div' ,class_='is-fs18 is-fBold')

def getId(info):

    m = []

    for i in info:

        force = repr(i).replace('is-fs18', '')

        m.append(re.sub(r'\D', '', force))

    return m

def rep(message):

    message = repr(message)

    if message == "'-'":
        return ['0','0','0']
    else: 
        return re.findall(r'\d+', message)

def get_(message):
    now = rep(message)

    return [now[0] + '.' + now[1], now[2]]

def getInfo(id='4320'):

    seasonBoat = requests.get('https://boatrace.jp/owpc/pc/data/racersearch/season?toban=' + id)
    soup1 = BeautifulSoup(seasonBoat.content, 'html.parser')

    info = {}

    boat_info = soup1.find_all('td')


    info["name"] = soup1.find_all(class_='racer1_bodyName')[0].text.replace('\u3000', ' ')
    info["name_kana"] = soup1.find_all(class_="racer1_bodyKana")[0].text.replace('\u3000', ' ')
    info["1"] = get_(boat_info[10].text)[0]
    info["2"] = get_(boat_info[11].text)[0]
    info["3"] = get_(boat_info[12].text)[0]
    info["4"] = get_(boat_info[13].text)[0]
    info["5"] = get_(boat_info[14].text)[0]
    info["6"] = get_(boat_info[15].text)[0]
    info["boatrace_point"] = boat_info[9].text.replace('-', '0')
    

    course = requests.get('https://www.boatrace.jp/owpc/pc/data/racersearch/course?toban=' + id)
    course_toban = BeautifulSoup(course.content, 'html.parser')

    course_info = course_toban.find_all(class_='table1_progress2Label')
    info["1_chance"] = course_info[6].text.replace('- -', '0').replace('%', '')
    info["2_chance"] = course_info[7].text.replace('- -', '0').replace('%', '')
    info["3_chance"] = course_info[8].text.replace('- -', '0').replace('%', '')
    info["4_chance"] = course_info[9].text.replace('- -', '0').replace('%', '')
    info["5_chance"] = course_info[10].text.replace('- -', '0').replace('%', '')
    info["6_chance"] = course_info[11].text.replace('- -', '0').replace('%', '')

    return info

def get_chance(info, course = 1) :
    chance_list = {}

    chance_1 = float(info["1"])
    chance_2 = float(info["2"])
    chance_3 = float(info["3"])
    chance_4 = float(info["4"])
    chance_5 = float(info["5"])
    chance_6 = float(info["6"])

    course_chance = float(info[str(count) + "_chance"])

    boatrace_point = float(info["boatrace_point"])

    chance_list["basic_chance"] = round(((chance_1 + chance_2 + chance_3) * boatrace_point) / course, 3)
    chance_list["course_chance"] = round(((chance_1 + chance_2 + chance_3) * course_chance),3)
    chance_list["total_chance"] = round(((chance_1 + chance_2 + chance_3) - (chance_4 + chance_5 + chance_6) / course) * 50, 3)

    return chance_list

##url = 'https://boatrace.jp/owpc/pc/race/racelist?rno=2&jcd=15&hd=20211119'
alive = id_from(url)

getID = getId(alive)

count = 0
list_all = []

print("次のURLからデータを取得します: " + url)

for id_integer in getID:
    count += 1

    info = getInfo(id_integer)

    id = str(count);

    info["count"] = count
    list_all.append(info)

    print("\n\n")
    print(id + "番: " + info["name"] + " (" + info["name_kana"] + ") " + "ID: " + id_integer)
    print("============データ============")
    print("１着率: " + info["1"] + "%")
    print("２着率: " + info["2"] + "%")
    print("３着率: " + info["3"] + "%")
    print("４着率: " + info["4"] + "%")
    print("５着率: " + info["5"] + "%")
    print("６着率: " + info["6"] + "%")
    print("コース別勝率: " + info[id + "_chance"] + "%")
    print("============データ============")

for data in list_all:

    result_chance = get_chance(data, data["count"])
    

    print("\n" + str(data["count"]) + "番 - (" + data["name"] + "): ")
    print("一般計算: " + str(result_chance["basic_chance"]) + "pt")
    print("コースポイント: " + str(result_chance["course_chance"]) + "pt")
    print("合計コースポイント: " + str(result_chance["total_chance"]) + "pt")
    print("指数: " + str(data["boatrace_point"] + "pt"))
