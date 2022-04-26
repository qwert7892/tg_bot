import requests
from bs4 import BeautifulSoup


def get_text(girl_sign, man_sign):
    dictionary = {
        'овен': 'oven',
        'весы': 'vesy',
        'козерог': 'kozerog',
        'рыбы': 'ryby',
        'дева': 'deva',
        'близнецы': 'bliznecy',
        'стрелец': 'strelec',
        'скорпион': 'skorpion',
        'водолей': 'vodolej',
        'лев': 'lev',
        'рак': 'rak',
        'телец': 'telec'
    }

    URL = f'https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/' \
          f'zhenshhina-{dictionary[str(girl_sign).lower().strip()]}' \
          f'-muzhchina-{dictionary[str(man_sign).lower().strip()]}/?updated'

    rs = requests.get(URL)
    root = BeautifulSoup(rs.content, 'html.parser')
    article = root.select_one('p')

    return article.text