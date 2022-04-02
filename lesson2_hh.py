from bs4 import BeautifulSoup as bs
import requests
import json
import pandas as pd
from pprint import pprint

base_url = 'https://hh.ru'
#текст для поиска (вместо пробелов используется знак'+')
text = 'data+analyst'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/100.0.4896.60 Safari/537.36'}

response = requests.get(base_url+'/search/vacancy?text='+text+'&area=1&salary=&currency_code=RUR&'
                        'experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&'
                        'no_magic=true&L_save_area=true', headers=headers).text

dom = bs(response, 'html.parser')

#найдем общее количество страниц поиска и запишем в переменную max_page
pages = dom.find_all('span',{'class':'pager-item-not-in-short-range'})
pages_list = []
for page in pages:
    number_page = page.find('a',{'class':'bloko-button'}).getText()
    pages_list.append(number_page)
max_page = int(pages_list[-1])

#создадим пустой список для вакансий
vacancies_list = []
#пройдем по всем страницам от 1ой до последней, равной переменной max_page
for i in range(max_page):
    response = requests.get(base_url+'/search/vacancy?text='+text+'&area=1&salary=&currency_code=RUR&'
                        'experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&'
                        'no_magic=true&L_save_area=true&page='+str(i)+'&hhtmFrom=vacancy_search_list', headers=headers).text

    dom = bs(response, 'html.parser')

    vacancies = dom.find_all('div',{'class':'vacancy-serp-item-body__main-info'})

    for vacancy in vacancies:
        vacancy_data = {}
        vacancy_name = vacancy.find('span', {'class': 'g-user-content'}).getText()
        if vacancy.find('span', {'class': 'bloko-header-section-3'}) != None:
            vacancy_salary = vacancy.find('span', {'class': 'bloko-header-section-3'}).getText().replace('\u202f', '')
            salary_list = vacancy_salary.split(' ')
            if salary_list[0] == 'от':
                vacancy_max_salary = None
                vacancy_min_salary = int(salary_list[1])
                vacancy_currency = salary_list[2]
            elif salary_list[0] == 'до':
                vacancy_max_salary = int(salary_list[1])
                vacancy_min_salary = None
                vacancy_currency = salary_list[2]
            else:
                vacancy_max_salary = int(salary_list[2])
                vacancy_min_salary = int(salary_list[0])
                vacancy_currency = salary_list[3]
        else:
            vacancy_max_salary = None
            vacancy_min_salary = None
            vacancy_currency = None
        vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_data['name'] = vacancy_name
        vacancy_data['max_salary'] = vacancy_max_salary
        vacancy_data['min_salary'] = vacancy_min_salary
        vacancy_data['currency'] = vacancy_currency
        vacancy_data['link'] = vacancy_link
        vacancies_list.append(vacancy_data)

with open('vacancy_hh.json', 'w') as file:
    json.dump(vacancies_list, file)
df = pd.read_json('vacancy_hh.json')
print(df)


