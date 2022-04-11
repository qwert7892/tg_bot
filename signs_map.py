import requests
from bs4 import BeautifulSoup

day = 1
month = 1
year = 1901

# URL = f'https://geocult.ru/natalnaya-karta-onlayn-raschet?fn=&fd={day}&fm={month}&fy={year}&fh=19&fmn=30&c1=%D0%9E%D1%80%D0%B5%D0%BD%D0%B1%D1%83%D1%80%D0%B3%2C+%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F&ttz=20&tz=Asia%2FYekaterinburg&tm=5&lt=51.7727&ln=55.0988&hs=P&sb=1'
URL = 'https://tragos.ru/natal-chart/11-april-2022-time-plus3-20-7-P-37.61556-55.75222-moscow'

response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')
soup_1 = soup.find_all('<p>')  # class_="natal_desc")

# print(soup.prettify())
# print(soup.prettify())
print(soup_1)
print(str(soup).split('<td'))
