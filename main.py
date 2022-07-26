import requests
from bs4 import BeautifulSoup

d = dict()


def getContent(html):
    souper = BeautifulSoup(html, 'html.parser')
    items = souper.find_all('div', class_='page-header')
    infoUser = souper.find_all('li', class_='list-group-item')
    # creates amazing username
    name = str(items[0])
    name_1 = name.replace('<div class="page-header">\n<h1>', "").replace("    <small></small>\n</h1>\n</div>", "") \
        .replace("<small>", "").replace("    ", " || ").replace('</small>\n</h1>\n</div>', '')
    d['name'] = name_1.replace('\n', "")

    # looks for constant things
    id = str(infoUser[0]).replace('<li class="list-group-item"><strong>ФШР ID</strong>: ', '').replace('</li>', '')
    d['id'] = id
    gender = str(infoUser[1]).replace('<li class="list-group-item"><strong>Пол</strong>: ', '').replace('</li>', '')
    d['gender'] = gender
    region = str(infoUser[2]).replace('<li class="list-group-item"><strong>Регион</strong>: ', '').replace('</li>', '')
    d['region'] = region.replace('\n              ', '').replace('\n            ', '')
    year = str(infoUser[3]).replace('<li class="list-group-item"><strong>Год рождения</strong>: ', '')\
        .replace('</li>', '')
    d['year'] = year
    otherParametrs = ""
    for i in range(4, len(infoUser)):
        otherParametrs += str(infoUser[i]).replace('<li class="list-group-item">\n<strong>', '').replace(
            '</strong>: ', "").replace('</li>', '').replace("\n             ", "") \
            .replace('\n          ', '').replace('<li class="list-group-item"><strong>'
                                                 '<span class="text-success">', "") \
            .replace("</span></strong>", "").replace("<b>", "").replace("</b>", "")\
            .replace('<li class="list-group-item"><strong><span class="text-danger">', "")\
            .replace('<li class="list-group-item"><strong><span class="text-primary">', "")\
            .replace('<li class="list-group-item">', "").replace('<strong>', "").replace('</strong>', "")\
            .replace('<span class="text-primary">', "").replace('<span class="text-success">', "")\
            .replace('<span class="text-danger">', "").replace("</span>", "").replace("</a>", "")\
            .replace('<a href="', "").replace('">', "*").replace("\n", "")
    parseOtherThings(otherParametrs)
    print(d)
    print(otherParametrs)


def parseOtherThings(other):
    if other.find("Разряд") != -1:
        grade = ""
        if other.find != "Гроссмейстер":
            grade = "Гроссмейстер"
        elif other.find != "Мастер спорта":
            grade = "Мастер спорта"
        else:
            for i in range(other.find("Разряд") + 6, len(other)):
                if other[i] == ")":
                    grade += ")"
                    break
                else:
                    grade += other[i]
        d['grade'] = grade
    if other.find("Классические") != -1:
        STD = ""
        for i in range(4):
            STD += other[other.find("Классические") + 23 + i]
        d['ruSTD'] = STD
    if other.find("Быстрые") != -1:
        RPD = ""
        for i in range(4):
            RPD += other[other.find("Быстрые") + 18 + i]
        d['ruRPD'] = RPD
    if other.find("Блиц") != -1:
        BLZ = ""
        for i in range(4):
            BLZ += other[other.find("Блиц") + 15 + i]
        d['ruBLZ'] = BLZ
    if other.find("std") != -1:
        STD = ""
        for i in range(4):
            STD += other[other.find("std") + 4 + i]
        d['fideSTD'] = STD
    if other.find("rpd") != -1:
        RPD = ""
        for i in range(4):
            RPD += other[other.find("rpd") + 4 + i]
        d['fideRPD'] = RPD
    if other.find("blz") != -1:
        BLZ = ""
        for i in range(4):
            BLZ += other[other.find("blz") + 4 + i]
        d['fideBLZ'] = BLZ
    if other.find("FIDE ID: ") != -1:
        link = ""
        for i in range(other.find("FIDE ID: ") + 9, len(other)):
            if other[i] == "*":
                break
            else:
                link += other[i]
        d['link'] = link
    if other.find("Звания: ") != -1:
        title = ""
        for i in range(other.find("Звания: ") + 8, len(other)):
            if other[i] == "Р":
                break
            else:
                title += other[i]
        d['title'] = title.replace("        ", "")
    if other.find("Федерация: ") != -1:
        federation = ""
        for i in range(3):
            federation += other[other.find("Федерация: ") + 11 + i]
        d['federation'] = federation


fhr_id = input("Введи айди ФШР:\n")
url = f"https://ratings.ruchess.ru/people/{fhr_id}"

htmler = requests.get(url=url)
getContent(htmler.text)
