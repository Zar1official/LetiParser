import requests
from bs4 import BeautifulSoup
from config import headers

def get_data(url ,headers):
    content= requests.get(url, headers).content
    soup  =BeautifulSoup(content, 'lxml')
    table=soup.find_all("table" , class_= "table table-bordered")
    snilses = table[0].find_all("td", class_="fio")
    numbers_of_place=table[0].find_all('td', class_="number")
    users_data=[]
    for i in range(len(snilses)):
        users_data.append({
            "number": numbers_of_place[i].text,
            "snils": snilses[i].text
        })
    return users_data

def get_number(user_snils, data):
    for i in data:
        if i['snils']==user_snils:
            return i['number']
    return None

def get_place(data, user_snils, n, type):
    counter=0
    place = None
    for k, v in data.items():
        if n == counter:
            places = get_data("https://etu.ru/" + data[k][type], headers)
            place = get_number(user_snils, places)
            break
        counter += 1
    return place