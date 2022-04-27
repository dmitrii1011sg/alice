from bs4 import BeautifulSoup
import requests


class Parser:
    def __init__(self, text):  # для инициализации класса нужно ввести поисковой текст типо автора ил названия
        self.base_url = 'https://ilibrary.ru'
        self.search = 'https://yandex.ru/search/?text='
        self.text = text
        self.text2 = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя., !'
        self.codec = ['%E0', '%E1', '%E2', '%E3', '%E4', '%E5', '%B8', '%E6', '%E7',
                      '%E8', '%E9', '%EA', '%EB', '%EC', '%ED', '%EE', '%EF', '%F0', '%F1', '%F2', '%F3',
                      '%F4', '%F5', '%F6', '%F7', '%F8', '%F9', '%FA', '%FB', '%FC', '%FD', '%FE',
                      '%FF', '.', '%2C', '+', '%21']
        self.session = requests.session()
        self.pages = 0

    def code(self):  # кодировка слова
        ans = str()
        for i in self.text:
            n = self.text2.index(i)
            ans += self.codec[n]
        return ans

    def first_page(self):  # парсинг первой страницы
        url1 = self.code()
        url = f'https://ilibrary.ru/search.phtml?q={url1}'
        soup = BeautifulSoup(self.session.get(url).text, 'html.parser')
        self.second_url = soup.li.a.get('href')
        stih = BeautifulSoup(self.session.get(self.base_url + self.second_url).text, 'html.parser')
        a = stih.find('div', class_='author')
        b = stih.find('div', class_='title')
        self.ans = a.text + b.text
        elements = stih.find('div', id='pmt1')
        for element in elements:
            self.ans += element.get_text()

        try:
            a = stih.find('div', class_='bnvin')
            self.pages = a.text.split('/')[1].split('Г')[0]
        except:
            pass

    def rearch(self):  # парсинг остальных страниц если есть
        self.first_page()
        if self.pages:
            a = self.second_url.split('/')[2]
            for i in range(2, int(self.pages) + 1):
                url = self.base_url + f'/text/{a}/p.{i}/index.html'
                page = self.session.get(url)
                stih = BeautifulSoup(page.text, 'html.parser')
                elements = stih.find('div', id='pmt1')
                for element in elements:
                    self.ans += element.get_text()

    def verse(self):  # выдача стиха
        self.rearch()
        return self.ans


a = Parser('бородино')  # example
print(a.verse())  # example