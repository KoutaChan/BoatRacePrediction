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

    res1 = requests.get('https://boatrace.jp/owpc/pc/data/racersearch/season?toban=' + id)
    soup1 = BeautifulSoup(res1.content, 'html.parser')

    ## 0 = 名前
    ## 1 = 1着
    ## 2 = 2着
    ## 3 = 3着
    ## 4 = 4着
    ## 5 = 5着
    ## 6 = 6着
    ## 7 = 能力指数
    ## 8 = 名前(カナ)
    ## 9 = コース別勝率(1)
    ## 10 = コース別勝率(2)
    ## 11 = コース別勝率(3)
    ## 12 = コース別勝率(4)
    ## 13 = コース別勝率(5)
    ## 14 = コース別勝率(6)

    ## \u3000 = スペース

    info = []

    boat_info = soup1.find_all('td')

    I1 = get_(boat_info[10].text)
    I2 = get_(boat_info[11].text)
    I3 = get_(boat_info[12].text)
    I4 = get_(boat_info[13].text)
    I5 = get_(boat_info[14].text)
    I6 = get_(boat_info[15].text)

    info.append(soup1.find_all(class_='racer1_bodyName')[0].text.replace('\u3000', ' '))
    info.append(I1[0])
    info.append(I2[0])
    info.append(I3[0])
    info.append(I4[0])
    info.append(I5[0])
    info.append(I6[0])
    info.append(boat_info[9].text.replace('-', '0'))
    info.append(soup1.find_all(class_="racer1_bodyKana")[0].text.replace('\u3000', ' '))

    res2 = requests.get('https://www.boatrace.jp/owpc/pc/data/racersearch/course?toban=' + id)
    soup2 = BeautifulSoup(res2.content, 'html.parser')

    course_info = soup2.find_all(class_='table1_progress2Label')
    info.append(course_info[6].text.replace('- -', '0').replace('%', ''))
    info.append(course_info[7].text.replace('- -', '0').replace('%', ''))
    info.append(course_info[8].text.replace('- -', '0').replace('%', ''))
    info.append(course_info[9].text.replace('- -', '0').replace('%', ''))
    info.append(course_info[10].text.replace('- -', '0').replace('%', ''))
    info.append(course_info[11].text.replace('- -', '0').replace('%', ''))

    return info

def chance_(info, course = 1):
    xp = (float(info[1]) + 5) + (float(info[2]) * 0.75) + (float(info[3]) * 0.45) - (float(info[6]) * 0.85) - (float(info[5]) * 0.6) - (float(info[4]) * 0.3)

    xp += 25
    ## low = 3
    if xp < 0: xp = 3
    return xp * (float(info[7]) + 50) * (float(info[8 + course]) + 1)
    ##計算式 (1着 + 5) + 2着 x 0.75 + 3着 x 0.45 - 6着 x 0.85 - 5着 x 0.6 - 4着 x 0.3 
    ## (合計値 + 15) x (能力指数 + 50) x (コース別成績 + 1)

def chance(info, course = 1):
    xp = (float(info[1]) + 5) + (float(info[2]) * 0.75) + (float(info[3]) * 0.45) - (float(info[6]) * 0.85) - (float(info[5]) * 0.6) - (float(info[4]) * 0.3) + (float(info[8 + course]) + 1)

    xp += 25
    ## low = 10
    if xp < 0: xp = 10
    return xp * (float(info[7]) + 50) 
    ##計算式 (1着 + 5) + 2着 x 0.75 + 3着 x 0.45 - 6着 x 0.85 - 5着 x 0.6 - 4着 x 0.3 + (コース別成績 + 1)
    ## (合計値 + 15) x (能力指数 + 50) 

def lite_chance(info, course = 1):
    xp = (float(info[1]) + 5) + (float(info[2]) * 0.75) + (float(info[3]) * 0.45) - (float(info[6]) * 0.85) - (float(info[5]) * 0.6) - (float(info[4]) * 0.3) + (float(info[8 + course]) + 1)

    xp += 25
    ## low = 10
    if xp < 0: xp = 10
    return xp * (float(info[7]) + 50) / (1 + course / 2.5)
    ##計算式 (1着 + 5) + 2着 x 0.75 + 3着 x 0.45 - 6着 x 0.85 - 5着 x 0.6 - 4着 x 0.3 + (コース別成績 + 1)
    ## (合計値 + 15) x (能力指数 + 50) / (1 + cource / 2.5)
##url = 'https://boatrace.jp/owpc/pc/race/racelist?rno=2&jcd=15&hd=20211119'
alive = id_from(url)

getID = getId(alive)

count = 0
nextL = []

print("次のURLからデータを取得します: " + url)

for i in getID:
    count += 1

    info = getInfo(i)

    nextL.append(info)

    print("\n\n")
    print(str(count) + "番: " + info[0] + " (" + info[8] + ") " + "ID: " + i)
    print("============データ============")
    print("１着率: " + info[1] + "%")
    print("２着率: " + info[2] + "%")
    print("３着率: " + info[3] + "%")
    print("４着率: " + info[4] + "%")
    print("５着率: " + info[5] + "%")
    print("６着率: " + info[6] + "%")
    print("コース別勝率: " + info[count + 8] + "%")
    print("============データ============")

count = 0
for i in nextL:
    count += 1
    
    nextGen = nextL[count - 1]

    point = round(chance_(nextGen, count))
    LBASE_POINT = round(chance(nextGen, count),3)
    LITE_POINT = round(lite_chance(nextGen, count),3)

    print("\n" + str(count) + "番: " + nextGen[0] + " (" + nextGen[8] + ") : " + str(point) + "pt" + "\n    裏ポイント合計: " + str(round(LBASE_POINT + LITE_POINT)) + "pt" + " (LBASE_POINT: " + str(LBASE_POINT) + "pt)" + " (LITE_POINT: " + str(LITE_POINT) + "pt)")