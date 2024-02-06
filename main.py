from sys import platform

import pandas as pd
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Для работы с клавиатурой

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from datetime import datetime, timedelta

import time
# from time import sleep
import pyautogui
import os
import requests
import json
import string


import pprint

from bs4 import BeautifulSoup
# import pandas as pd
import itertools

from urllib.parse import urlencode  # Для генерации url, который работает через Proxy


class constructor():

    def __init__(self,
                 name_website="dns",  # имя сайта на английском
                 name_product="Смартфон",  # наименование продукта
                 url_product="",  # url первой страницы поиска
                 encoding="",
                 name_tag="",
                 name_class="",


                 web_driver="",  # расположение chromedriver.exe
                 path_downloads="",  # путь до папки "Загрузки"
                 separator_for_path='',
                 use_proxy=False,  # использование proxy при работе
                 list_proxy=list(),  # список доступных proxy

                #  name_teg_last_page="a",  # тег номера последней страницы, отображ-ся на сайте
                #  name_attribute_last_page="class",  # по какому атрибуту искать номер последней страницы (class/role)
                #  name_class_last_page="pagination-widget__page-link",
                #  # имя класса номера последней страницы, отображ-ся на сайте
                #  button_text_new_page="Показать ещё",  # текст на кнопке, которая переводит на след. страницу поиска
                
                 tag_link_next_page = '', # Тег внутри которого лежит ссылка на новую страницу
                 class_link_next_page = '' # Класс внутри которого лежит ссылка на новую страницу

                 
                 ):

        # сведения для скачивания страниц

        # Переданные параметры для chromedriver и папки Загрузки
        self.web_driver = web_driver
        self.path_downloads = path_downloads
        self.separator_for_path = separator_for_path

        # местоположение chromedriver
        if web_driver == "":  # если параметр не задан
            if platform == "linux" or platform == "linux2":
                self.web_driver = "/home/ingvar/PycharmProjects/parser/parsing_constructor/chromedriver_linux64/chromedriver"
            elif platform == "win32":
                self.web_driver = "C:\\Users\\Ingvar\\PycharmProjects\\parsing_constructor\\chromedriver_win64\\chromedriver.exe"

        # путь до папки "Загрузки"
        if path_downloads == "":  # если параметр не задан
            if platform == "linux" or platform == "linux2":
                self.path_downloads = "/home/ingvar/Загрузки"
            elif platform == "win32":
                self.path_downloads = "C:\\Users\\Ingvar\\Downloads"

        # разделитель для указания пути к файлам\папкам
        if separator_for_path == "":  # если параметр не задан
            if platform == "linux" or platform == "linux2":
                self.separator_for_path = "/"
            elif platform == "win32":
                self.separator_for_path = "\\"

        # общие сведения
        self.name_website = name_website  # имя сайта, с которым работаем,
        self.name_product = name_product  # имя товара, например: телефон, пылесос
        self.url_product = url_product  # ссылка на раздел исследуемого товара
        self.encoding = encoding  # кодировка страницы товара
        self.name_tag = name_tag
        self.name_class = name_class



        self.tag_link_next_page = tag_link_next_page # Тег внутри которого лежит ссылка на новую страницу
        self.class_link_next_page = class_link_next_page # Класс внутри которого лежит ссылка на новую страницу

        # self.name_teg_last_page = name_teg_last_page  # тег номера последней страницы, отображ-ся на сайте
        # self.name_attribute_last_page = name_attribute_last_page  # по какому атрибуту искать номер последней страницы (class/role)
        # self.name_class_last_page = name_class_last_page  # имя класса номера последней страницы, отображ-ся на сайте
        # self.button_text_new_page = button_text_new_page  # текст на кнопке, которая переводит на след. страницу поиска
        
        

        self._url_server = "https://35a4-89-179-47-36.eu.ngrok.io/api/information/"
        self.use_proxy = use_proxy
        self._tree_dom_bs4 = None
        self._list_rules = []
        self.buttons_data = []

    def get_proxy_url(self, API_KEY, url):
        """
        Источник: https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-find-elements-xpath/
        В самом конце находилась эта функция.

        НЕ ДО КОНЦА ЯСНО, КАК ЕЁ ПРИМЕНЯТЬ
        """
        API_KEY = "YOUR-SUPER-SECRET-API-KEY"
        payload = {
            "api_key": API_KEY,
            "url": url
        }
        # кодируем url, который вы хотите получить, и объединяем его с url прокси-сервера
        proxy_url = "Url сайта, например https://proxy.scrapeops.io/v1/?" + urlencode(payload)
        # возвращает url сайта, переданного через прокси
        return proxy_url


    def get_request(self, dict_result={}):
        
        if not(dict_result): # если словарь пуст
            
            'https://a2da-89-179-47-18.eu.ngrok.io/api/information/'

            if "api/information" in self._url_server:
                get_result = requests.get(self._url_server)
                # print(get_result.text)
                dict_result = dict(get_result.json())
            else:
                print("В названии ссылки на сервер отсутствует в конце api/information")
                return 0

        """Единожды / one"""

        # общие сведения
        self.name_website = dict_result['designer']['one']['site']
        self.name_product = dict_result['designer']['one']['type_product']
        self.url_product = dict_result['designer']['one']['url']

        self.name_tag = dict_result['designer']['one']['teg_name_url']
        self.name_class = dict_result['designer']['one']['class_name_url']

        # сведения для скачивания страниц
        self.tag_link_next_page = dict_result['designer']['one']['teg_name_number']
        self.class_link_next_page = dict_result['designer']['one']['class_name_number']

        # self.name_teg_last_page = dict_result['designer']['one']['teg_name_number']
        # self.name_attribute_last_page = dict_result['designer']['one']['role_name_url']
        # self.name_class_last_page = dict_result['designer']['one']['class_name_number']
        # self.button_text_new_page = dict_result['designer']['one']['name_button']

        """Многократно / many"""

        self.buttons_data = dict_result['designer']['buttons']


        temp = dict_result['designer']['many']
        print(f"Число правил для товара: {len(temp)}")
        # for dict_param in temp:
        #     print(f"{dict_param['title']} : {len(dict_param['title'])}")
        #     print(f"{dict_param['teg_name']}: {len(dict_param['teg_name'])}")
        #     print(f"{dict_param['class_name']} : {len(dict_param['class_name'])}")

        # сведения по заголовку хар-ки
        self._list_rules = dict_result['designer']['many']  # список из словарей, ключами являются название хар-ки, тег и аттрибуты

    def download_links(self):
        """
            Метод для вытаскивания ссылок из страниц товаров

        """
        type_value = "href"

        files = os.listdir(self.path_downloads + self.separator_for_path + self.name_website)
        count_sait = list(filter(lambda x: x.endswith('.html'), files))
        # print("count_sait", count_sait)
        num_page_old = len(count_sait)  # кол-во скачанных страниц, из к-х нужно доставать ссылки
        
        for i in range(0, num_page_old):
            name_file = self.name_website + str(i) + '.html'

            with open(
                    self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + name_file,
                    "r",
                    encoding='utf-8') as html_file:
                self._tree_dom_bs4 = BeautifulSoup(html_file, 'lxml')

            # поиск тегов  с определенным классом по дереву
            if self.name_tag != "" and self.name_class != "":
                Nodes = self._tree_dom_bs4.find_all(self.name_tag, class_=self.name_class)

            elif self.name_tag != "" and self.name_class == "":
                Nodes = self._tree_dom_bs4.find_all(self.name_tag)

            one_family_for_elements = 0
            for i in range(len(Nodes)):
                #print(Nodes[i].prettify())
                
                # Если имя продукта содержится в названии объявления в нижнем регистре
                if (self.name_product.lower()) in Nodes[i].text.lower(): 
                    if 'href' in Nodes[i].attrs: # доходим до первого подходящего кандидата, чтобы найти родителя
                        one_family_for_elements = Nodes[i].parent # сохраняем семейство этих ссылок и работаем с ними
                        #print(Nodes[i].prettify(),"\n\n")
                        #print(one_family_for_elements.prettify())
                        break
            
            # берем только одно семейство для извлечения ссылок
            if self.name_tag != "" and self.name_class != "":
                Nodes = one_family_for_elements.find_all(self.name_tag, class_=self.name_class)
                
            elif self.name_tag != "" and self.name_class == "":
                Nodes = one_family_for_elements.find_all(self.name_tag)
                        

            with open(
                    self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + "product_links.txt",
                    "a",
                    encoding='utf-8') as file:
                for i in range(len(Nodes)):
                    #print(Nodes[i].prettify())
                    #print(f"Модель: {Nodes[i].text}")kk
                    if (self.name_product.lower()) in Nodes[i].text.lower(): # Все в нижнем регистре
                        
                        if 'href' in Nodes[i].attrs:
                            temp_link = Nodes[i][type_value]
                            main_piece_url = ""
                            

                            # Проверка, что ссылка полная
                            if "https://" in temp_link:
                                if self.name_website in temp_link:
                                    pass
                            elif "http://" in temp_link:
                                if self.name_website in temp_link:
                                    pass
                            else:
                                http_or_s = 0
                                if "https://" in self.url_product:
                                    http_or_s = len("https://")
                                elif "http://" in self.url_product:
                                    http_or_s = len("http://")
                                index_end = self.url_product[http_or_s:].find("/")
                                # print()
                                main_piece_url = self.url_product[:http_or_s + index_end]

                            file.write(main_piece_url + temp_link + "\n")

    """
    def collections_title_value(tree_BS4, current_DataBase: pd.DataFrame, path: str):
        names_classes = {'title': 'product-characteristics__spec-title',
                         'value': 'product-characteristics__spec-value'}
        # TR = Translator(from_lang="ru", to_lang="en")
        stringe = str()
        Nodes = tree_BS4.find_all("div",
                                  class_="product-characteristics__group")  # поиск объекта с группами характеристик
        example_type = type(tree_BS4.find('div'))  # для проверки типа "Tag" и наличия метода attrs
        current_columns = current_DataBase.columns  # столбцы текущей БД, которую передали как параметр
        unused_names_columns = current_DataBase.columns
        # print(type(unused_names_columns))
        list_unused_names_columns = list(unused_names_columns)

        # буферная однострочная БД для склеивания с текущей,
        # создается на основе столбцов текущей БД
        buffer_DataBase = pd.DataFrame(columns=current_columns)

        #Сбор характеристик по DOM-дереву конкретного телефона
        # по каждой группе с харатеристиками
        for i in range(len(Nodes)):
            # print(f"{Nodes[i].text:>50} ,\n")
            # print(Nodes[i].prettify())
            # print(Nodes[i].prettify())
            List_child = Nodes[i].descendants
            # print("List_child: ", len(list(List_child)))
            count = 0

            flag_title = False
            flag_value = False
            name_title = str()
            value_title = str()

            # Прямой дочерний элемент - это дочерний элемент,
            # который находится непосредственно под родительским
            # элементом с точки зрения иерархии. То есть не внук или правнук.
            # print(f"{Nodes[i].text:>50} ,\n")
            # по каждому полю в группе
            TITLE_None = 0
            for child in List_child:
                # print(count, end=" ")
                # count += 1
                # print("\t ", type(child), ": ", child, "\n")

                # Проверка на то, что это тэг и у него будет метод attrs
                if type(child) is example_type:
                    if 'class' in child.attrs:
                        # print(child.attrs)
                        # print(names_classes['title'] in child['class'])
                        if names_classes['title'] in child['class']:  # a in b, a-строка, b-список
                            # print(child.string)
                            if child.string is None:
                                # создание среза из генератора дочерних элементов, для перехода к следующему
                                list_name_title = list(
                                    itertools.islice(Nodes[i].descendants, TITLE_None + 1, TITLE_None + 2))
                                name_title = list_name_title[0]
                                flag_title = True

                                # t1 = Class_Timer.Timer()
                                # t1.start()
                                # res = TR.translate(name_title)
                                # t1.stop()
                                # print("title: ", name_title)
                                # stringe = " ".join([stringe,name_title])
                                # print(stringe)
                            else:
                                # name_title = child.string # не работает, так как берет None, вместо строки
                                name_title = child.string

                                # stringe = " ".join([stringe,name_title])
                                flag_title = True
                                # print("title", name_title)
                                # print(stringe)
                        elif names_classes['value'] in child['class']:
                            value_title = child.string
                            flag_value = True
                            # print("value: ", value_title) # .encode('utf-8'))

                        if flag_title and flag_value:
                            if value_title is None:
                                value_title = 'Перечисление'
                            temp_value = value_title.encode('utf-8').decode('utf-8')

                            if (name_title in list_unused_names_columns):  # Удаление использованных имен столбцов
                                list_unused_names_columns.remove(name_title)

                            # удаление пробелов
                            temp_value = temp_value.lstrip()
                            temp_value = temp_value.rstrip()
                            temp_name = name_title
                            temp_name = temp_name.lstrip()
                            temp_name = temp_name.rstrip()
                            buffer_DataBase[temp_name] = [temp_value]  # .replace(" ", "")
                            flag_title = False
                            flag_value = False

                # print("child.string = ", child.string, end="\n\n")
                # print("\n\n")
                TITLE_None += 1
            # print("\n\n")

        # Подсчет кол-во новых столбцов
        old_and_new_columns = buffer_DataBase.columns
        count_current_columns = len(current_columns)
        count_old_and_new_columns = len(old_and_new_columns)
        count_new_columns = count_old_and_new_columns - count_current_columns  # нашел число новых столбцов

        # Извлечение имен новых столбцов
        # Чтобы достать названия новых столбцов, мне необходимо закинуть старые и новые столбцы в структуру Series,
        # далее при помощи числовых индексов и знания кол-ва "старых"(текущих) стобцов вытащить их имена

        # Пример:
        # текущая БД -> 75 столбцов, ,буферная БД -> 77 столбцов
        # Число новых столбцов = 77 - 75 = 2
        # index_new_columns = list(Series_new_columns[count_current_columns:].index) -> [76,77]
        # Из Series с пронумерованными названиями столбцов буферной БД извлекаю названия под номерами 76 и 77
        # Добавляю новые столбцы к текущей БД с пустыми ячейками заданной длины(длина = последний индекс в текущей БД)
        #
        # а

        Series_new_columns = pd.Series(
            old_and_new_columns)  # формирую Series на основе имеющихся столбцов из буферной БД

        # Беру срез из Series, начиная с последнего столбца текущей БД +1
        # Вытаскиваю индексы "новых" столбцов и формирую из них список
        index_new_columns = list(Series_new_columns[count_current_columns:].index)
        names_new_columns = list()
        for i in index_new_columns:
            names_new_columns.append(Series_new_columns[i])

        # Добавление новых столбцов к текущей БД и заполнение для старых телефонов каждой ячейки нового столбца затычкой
        # кол-во ячеек в столбцах
        temp = list(current_DataBase.index)
        if len(temp):
            count_box = temp[-1] + 1  # индекс последней строки в текущей БД
        else:
            count_box = 0
        list_empty = [""] * count_box

        DF_list_empty = pd.DataFrame(list_empty, columns=[name])

        # добавление пустых столбцов к текущей БД
        for name_column in names_new_columns:
            DF_list_empty = pd.DataFrame(list_empty, columns=[name_column])
            current_DataBase = pd.concat([current_DataBase, DF_list_empty], axis=1)
            # current_DataBase[name_column] = list_empty

        # Конкатенация буферной БД и текущей
        # print("Текущая БД: ", current_DataBase)
        # print("Буферная БД: ",buffer_DataBase)
        current_DataBase = pd.concat([current_DataBase, buffer_DataBase], ignore_index=True)

        flag_print = False
        keys = current_DataBase.columns
        if flag_print:
            for key in keys:
                print(f"{current_DataBase[key]}\n")
        # t1 = Class_Timer.Timer()
        # t1.start()
        # res = TR.translate(stringe)
        # t1.stop()
        # print(res)

        # if len(unused_names_columns): # если остались неиспользованные имена столбцов
        #     last_index = current_DataBase.index[-1]
        #     for name_column in unused_names_columns: # для каждого имени вставляем затычку
        #         current_DataBase[name_column, last_index] = ""
        return current_DataBase
    """


    def download_pages(self):

        # Создание/переименовывание папки, в которой будут лежать скачанные страницы
        if not os.path.isdir(self.path_downloads + self.separator_for_path + self.name_website):
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website)
        else:
            os.rename(self.path_downloads + self.separator_for_path + self.name_website,
                      self.path_downloads + self.separator_for_path + self.name_website + str(datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website)

        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)  # запустить браузер

        stealth(driver,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        driver.implicitly_wait(1)
        driver.maximize_window()  # открыть окно браузера на весь экран

        try:
            driver.get(self.url_product)  # перейти по ссылке URL
            # my_wait(driver, 0.1, 30)
            
            # Сохранение первой страницы из N штук
            page = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")
            
            
            number_of_pages = 1
            name = self.name_website + str(number_of_pages-1) + '.html'  # Имя страницы


            # Проверка в page на наличие кнопки перехода на следующую страницу
            html_page = BeautifulSoup(page, 'lxml')
            
            # Поиск кнопки перехода на следующую страницу
            next_page_list = html_page.find_all(self.tag_link_next_page, class_=self.class_link_next_page)
            
            next_page_link = ''
            if next_page_list: # Если есть кандидаты с ссылкой на следующую страницу
                for i in range(len(next_page_list)):
                    if 'href' in next_page_list[i].attrs:
                        next_page_link = next_page_list[i]['href']


            
            with open(self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + name, "w",
                      encoding="utf-8") as file:
                file.write(page)

            time.sleep(5)

            flag_not_click = 0

            while (True): # Пока получается найти кнопку перехода на следующую страницу, работаем
                
                if next_page_link:
                    #print(f"Переход на следующую страницу: {next_page_link}")
                    
                    # Переходим на следующую страницу и сохраняем её.
                    try:
                        time.sleep(3)
                        #print("------------------")
                        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="' + self.button_text_new_page + '" and not(@disabled)]')))
                        time.sleep(2)

                        # Переходим на следующую страницу нажатием кнопки перехода
                        Xpath_next_page = '//' + self.tag_link_next_page + '[@class="'+ self.class_link_next_page + '"]'
                        driver.find_element(By.XPATH,Xpath_next_page).click()
                         

                    except:
                        print("Not click: Переход не был осуществлен", number_of_pages) # Перехода не было
                        flag_not_click += 1
                        break
                    
                    else: # Если ошибок в блоке try не возникло, выполнится код ниже


                        number_of_pages += 1
                        name = self.name_website + str(number_of_pages-1) + '.html'
                        # my_wait(driver, 0.1, 30)

                        # Изъяли HTML код нужной страницы 
                        page = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")

                        # Проверяем наличие кнопки перехода в конце бесконечного цикла
                        html_page = BeautifulSoup(page, 'lxml')
                        
                        # Поиск кнопки перехода на следующую страницу
                        next_page_list = html_page.find_all(self.tag_link_next_page, class_=self.class_link_next_page)
                        
                        next_page_link = ''
                        if next_page_list: # Если есть кандидаты с ссылкой на следующую страницу
                            for i in range(len(next_page_list)):
                                if 'href' in next_page_list[i].attrs:
                                    next_page_link = next_page_list[i]['href']

                        # Записали в файл скачанный HTML код
                        with open(self.path_downloads + self.separator_for_path + self.name_website + "\\" + name, "w",
                                    encoding="utf-8") as file:
                            file.write(page)

                        time.sleep(1)
                        

                        print("Номер сохраненной страницы =", number_of_pages)

                else:
                    print(f"Либо нас заблокировали, либо это последняя страница: {next_page_link}")
                    break

        except Exception as ex:
            print(ex)
            print("При скачивании страниц возникла проблема")
        finally:
            driver.quit()

    def download_unic_pages(self):

        if not os.path.isdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic'):
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')
        else:
            os.rename(self.path_downloads + self.separator_for_path + self.name_website + '_unic',
                      self.path_downloads + self.separator_for_path + self.name_website + '_unic' + str(
                          datetime.now().date()) +
                      '_' + str(datetime.now().microsecond))
            os.mkdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')

        unic_url = list()

        with open(
                self.path_downloads + self.separator_for_path + self.name_website + self.separator_for_path + "product_links.txt",
                "r",
                encoding='utf-8') as file:
            
            for line in file:
                # unic_url.append(self.head_url + line)
                unic_url.append(line)

        s = Service(self.web_driver)
        driver = webdriver.Chrome(service=s)  # запустить браузер

        stealth(driver,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True
                )

        driver.implicitly_wait(1)
        driver.maximize_window()  # открыть окно браузера на весь экран

        for i in range(0, len(unic_url)):
            # перейти по ссылке URL
            driver.get(unic_url[i])

             # self.buttons_data - Выкладываю данные про кнопки с общего массива данных

            try: # для каждой страницы нажимаем группу кнопок (массив словарей с данными)
                for button_data in self.buttons_data: # идем по списку кнопок
                    try: # пробуем поочередно нажать на кнопки
                        time.sleep(2)

                        Xpath_button = '//' + button_data["teg_name"] + '[@class="'+ button_data["class_name"] + '" and not(@disabled)]'
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Xpath_button)))
                        time.sleep(2)
                        candidates_buttons = driver.find_elements(By.XPATH, Xpath_button)
                        for index_button in range(len(candidates_buttons)): # проходим по всем найденным кнопкам
                            if button_data["button_text"] in candidates_buttons[index_button].text: # если это подходящая кнопка
                                candidates_buttons[index_button].click()
                                # print(f"Нажата клавиша {candidates_buttons[i].text}")
                                # print("\n\n")

                    except: # если не получилось нажать на кнопку
                        continue
                   
            except:
                print("Not click Не получилось нажать кнопку развертывания характеристик или фото")
                continue

            try:
                time.sleep(2)
                name = self.name_website + '_unic_' + str(i) + '.html'
                page = driver.find_element(By.XPATH, "//body").get_attribute("outerHTML")
                with open(
                        self.path_downloads + self.separator_for_path + self.name_website + '_unic' + self.separator_for_path + name,
                        "w",
                        encoding="utf-8") as file:
                    file.write(page)
                time.sleep(2)

            except Exception as ex:
                print("Ошибка при сохранении файла с outerHTML")
                print(ex)

            
        driver.quit()

    def extraction_data_BS4(self):

        files = os.listdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')
        list_files = list(filter(lambda x: x.endswith('.html'), files))
        print(f"Кол-во скачанных страниц товара: {len(list_files)}")
        temp_dict = dict()
        dict_for_post_request = dict()
        dict_for_post_request['site'] = self.name_website
        dict_for_post_request['type_product'] = self.name_product
        
        for rule in self._list_rules:
            temp_dict[rule['name_column']] = list()
        temp_dict["Источник"] = list()

        # По всем скачанным файлам товара
        for name_file in list_files:
            # name = self.name_website + '_unic_' + str(i) + '.html'
            with open(
                    self.path_downloads + self.separator_for_path + self.name_website + '_unic' + self.separator_for_path + name_file,
                    'r', encoding="utf-8") as html_file:
                self._tree_dom_bs4 = BeautifulSoup(html_file, "lxml")

            list_unused_name = list(temp_dict.keys())
            # По всем полученным правилам
            for rule in self._list_rules:


                str_all = str()
                Nodes_all = self._tree_dom_bs4.find_all(rule['teg_name'], class_=rule['class_name'])
                # print(len(Nodes_all))

                for i in range(len(Nodes_all)):
                    temp_str = Nodes_all[i].text

                    if rule['title'].lower() in temp_str.lower():
                        list_unused_name.remove(rule['name_column'])
                        str_all = str(temp_str).replace("  ", " ")
                        str_all = " ".join(str_all.split())
                        break


                temp_dict[rule['name_column']].append(str_all[:])

            temp_dict["Источник"].append(name_file) # потом удалить, все что связано с источником, весь столбец

            # По всем неиспользованным именам хар-тик из правил
            # print(f"Лист {list_unused_name}")
            # for unused_name in list_unused_name:
            #     print(temp_dict[unused_name])
            #     temp_dict[unused_name].append("")  # вставить заглушки

        dict_for_post_request['data'] = temp_dict
        #print(json.dumps(dict_for_post_request['data'], sort_keys=False, indent=4, ensure_ascii=False))
        #print(dict_for_post_request['data'].keys())

        df = pd.DataFrame(columns=dict_for_post_request['data'].keys())
        print(dict_for_post_request['data'].keys())
        for key in dict_for_post_request['data'].keys():
            df[key] = dict_for_post_request['data'][key] # При одинаковом числе объявлений разное число характеристик
            #print(f"key: {key} => {len(dict_for_post_request['data'][key][:len(dict_for_post_request['data']["Продажа"])])}")

        for index_str in df.index:
            print(df.iloc[index_str])
            print("\n")



        # url = "https://35a4-89-179-47-36.eu.ngrok.io/api/information/"
        # dict_for_post_request = json.dumps(dict_for_post_request)
        # r = requests.post(self._url_server, data=dict_for_post_request, headers={'Content-Type': 'application/json'})
        # print(r)





    def extraction_data(self):

        files = os.listdir(self.path_downloads + self.separator_for_path + self.name_website + '_unic')
        list_files = list(filter(lambda x: x.endswith('.html'), files))

        print(f"Кол-во скачанных страниц товара: {len(list_files)}")
        temp_dict = dict()
        dict_for_post_request = dict()
        dict_for_post_request['site'] = self.name_website
        dict_for_post_request['type_product'] = self.name_product

        for rule in self._list_rules:
            temp_dict[rule['name_column']] = list()
        temp_dict["Источник"] = list()


        # По всем скачанным файлам товара
        for name_file in list_files:
            options = Options()
            options.add_argument("--headless=new") # for Chrome >= 109


            s = Service(self.web_driver)
            driver = webdriver.Chrome(service=s, options=options)  # запустить браузер

            stealth(driver,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True
                    )


            # name = self.name_website + '_unic_' + str(i) + '.html'
            path_to_page = self.path_downloads + self.separator_for_path + self.name_website + '_unic' + self.separator_for_path + name_file


            list_unused_name = list(temp_dict.keys())
            driver.get(path_to_page)
            print(path_to_page)
            try:
                # По всем полученным правилам
                for rule in self._list_rules:

                    str_all = str()

                    #time.sleep(2)

                    XPATH = '//' + rule["teg_name"] + '[@class="' + rule['class_name'] + '"]'
                    #WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, XPATH)))
                    # time.sleep(2)
                    Nodes_all = driver.find_elements(By.XPATH, XPATH)

                    # (self._tree_dom_bs4.find_all(rule['teg_name'], class_=rule['class_name']))
                    # print(len(Nodes_all))

                    for i in range(len(Nodes_all)):
                        temp_str = Nodes_all[i].text

                        if rule['title'].lower() in temp_str.lower():
                            list_unused_name.remove(rule['name_column'])
                            str_all = str(temp_str).replace("  ", " ")
                            str_all = " ".join(str_all.split())
                            break


                    temp_dict[rule['name_column']].append(str_all[:])
                    # print(f"{'name_column'}:{str_all[size_title:]}")

            except Exception as ex:
                print("-Неудачно")
                print(ex)
            finally:
                driver.close()

            temp_dict["Источник"].append(name_file)  # потом удалить, все что связано с источником, весь столбец
            # По всем неиспользованным именам хар-тик из правил
            # for unused_name in list_unused_name:
            #    temp_dict[unused_name].append("")  # вставить заглушки

        driver.quit()
        dict_for_post_request['data'] = temp_dict

        df = pd.DataFrame(columns=dict_for_post_request['data'].keys())
        for key in dict_for_post_request['data'].keys():
            df[key] = dict_for_post_request['data'][key] # При одинаковом числе объявлений разное число характеристик
            #print(f"key: {key} => {len(dict_for_post_request['data'][key][:len(dict_for_post_request['data']["Объявление"])])}")

        for index_str in df.index:
            print(df.iloc[index_str])
            print("\n")
        #print(json.dumps(dict_for_post_request['data'], sort_keys=False, indent=4, ensure_ascii=False))
        for key in dict_for_post_request['data'].keys():
            print(f"key: {key} => {len(dict_for_post_request['data'][key])}")
        # url = "https://35a4-89-179-47-36.eu.ngrok.io/api/information/"
        # dict_for_post_request = json.dumps(dict_for_post_request)
        # r = requests.post(self._url_server, data=dict_for_post_request, headers={'Content-Type': 'application/json'})
        # print(r)

    def parsing_process(self):

        # Запрос на получение данных, их запись в атрибуты класса
        self.get_request()

        # Скачивание страниц с товаром
        self.download_pages()

        # Изъятие ссылок и запись их в файл
        self.download_links()

        # Скачивание страниц товара
        self.download_unic_pages()

        # Изъятие характеристик из скачанных страниц товара
        self.extraction_data()

# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
def create_dict_rules():

    dict_rules = {"designer": 
        {
            'one': {'site':'', 
                    'type_product':'',
                    'url':'',
                    'teg_name_url':'',
                    'class_name_url':'',
                    'teg_name_number':'',
                    'class_name_number':''
                    },

            'buttons': [  {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'ПТС'},
                                            {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'о регистрации'},
                                            {'teg_name': 'button', 'class_name': 'ezmft1z0 css-xst070 e104a11t0', 'button_text': 'фото'},
                                            {'teg_name': 'button', 'class_name': 'css-18zgczx e3cb8x01', 'button_text': 'контакты'}],

            'many': [] 
        }
    }


    
    # общие сведения
    dict_rules['designer']['one']['site'] = 'drom'
    dict_rules['designer']['one']['type_product'] = 'лада'
    dict_rules['designer']['one']['url'] = 'https://novorossiysk.drom.ru/lada/2110/?unsold=1&distance=100",  # 2 страницы 38 объявлений'

    dict_rules['designer']['one']['teg_name_url'] = 'a' # тег ссылки на машину в общем списке ссылок
    dict_rules['designer']['one']['class_name_url'] = 'css-1oas0dk e1huvdhj1' # класс ссылки на машину в общем списке ссылок

    # сведения для скачивания страниц
    dict_rules['designer']['one']['teg_name_number'] = 'a'   # self.tag_link_next_page
    dict_rules['designer']['one']['class_name_number'] = 'css-4gbnjj e24vrp30' # self.class_link_next_page


    # сведения для поиска и нажатия кнопок при скачивании страниц
    dict_rules['designer']['buttons'] = [   {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'ПТС'},
                                            {'teg_name': 'button', 'class_name':'e8vftt60 css-1uu0zmh e104a11t0', 'button_text': 'о регистрации'},
                                            {'teg_name': 'button', 'class_name': 'ezmft1z0 css-xst070 e104a11t0', 'button_text': 'фото'}]


    # сведения для скачивания характеристик
    dict_rules['designer']['many'] = [
        {'title':'Продажа', 'teg_name':'div', 'class_name':'css-987tv1 eotelyr0','name_column':'Объявление'},
        {'title': '₽', 'teg_name': 'div', 'class_name': 'css-eazmxc e162wx9x0', 'name_column':'Цена'},
        {'title': 'цена', 'teg_name': 'div', 'class_name': 'css-1pubr08 e93r9u20','name_column':'Сравнение цены'},
        {'title': 'ПТС', 'teg_name': 'button', 'class_name': 'e8vftt60 css-1uu0zmh e104a11t0', 'name_column':'Характеристики'},
        {'title': 'регистрац', 'teg_name': 'button','class_name': 'e8vftt60 css-1uu0zmh e104a11t0','name_column':'Регистрации'},
        {'title': 'розыск', 'teg_name': 'div', 'class_name': 'css-13qo6o5 e1mhp2ux0','name_column':'Розыск'},
        {'title': 'огранич', 'teg_name': 'div', 'class_name': 'css-13qo6o5 e1mhp2ux0', 'name_column':'Ограничения'}
                                     ] # список из словарей, ключами являются название хар-ки, тег и аттрибуты

    return dict_rules


### ПРОВЕРКА РАБОТЫ МЕТОДА download_pages()

'''drom = constructor(name_website="drom",
                   name_product="лада",
                   url_product="https://novorossiysk.drom.ru/lada/2110/?unsold=1&distance=100",  # 2 страницы 38 объявлений
                   tag_link_next_page="a",
                   class_link_next_page="css-4gbnjj e24vrp30",
                  )
drom.download_pages()
'''


### ПРОВЕРКА РАБОТЫ МЕТОДА download_links()
"""
drom = constructor(name_website="drom",
                   name_product='лада',
                   name_tag="a",                        # тег ссылки на машину в общем списке ссылок
                   name_class="css-1oas0dk e1huvdhj1")  # класс ссылки на машину в общем списке ссылок
drom.download_links()
"""

### ПРОВЕРКА РАБОТЫ МЕТОДА download_unic_pages()

drom = constructor()
dict_rules = create_dict_rules()
drom.get_request(dict_result=dict_rules)

drom.extraction_data_BS4()
drom.extraction_data()















# _______________________________________________________________________________________


"""
with open("C:\\Users\\Ingvar\\Downloads\\eldo.html",'r', encoding='utf-8') as name_html:
    soup = BeautifulSoup(name_html, 'lxml')
    res = soup.find_all('a', role="button")
    list_last_page = list()
    for i in range(len(res)):
        temp_num = res[i].text
        if temp_num.isdigit():
            list_last_page.append(int(temp_num))
            #print(f"Атрибуты: {res[i].attrs}\n\n")
    print(f"Номер последней страницы: {max(list_last_page)}")
"""



# url_Danil = 'https://a2da-89-179-47-18.eu.ngrok.io/api/information/'
# r_full = requests.get(url_Danil)
# r = dict(r_full.json())
#
# obj = constructor(name_website=r['designer']['one']['site'],
#                   name_product=r['designer']['one']['type_product'],
#                   url_product=r['designer']['one']['url'],
#                   name_teg_last_page=r['designer']['one']['teg_name_number'],
#                   name_attribute_last_page=r['designer']['one']['role_name_url'],
#                   name_class_last_page=r['designer']['one']['class_name_number'],
#                   button_text_new_page=r['designer']['one']['name_button'])

'''
obj = constructor(name_website="dns",
                  name_product="Смартфон",
                  url_product="https://www.dns-shop.ru/search/?q=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD%D1%8B+xiaomi+poco&category=17a8a01d16404e77",
                  name_teg_last_page="a",
                  name_attribute_last_page="class",
                  name_class_last_page="pagination-widget__page-link",
                  button_text_new_page="Показать ещё")'''






"""

files = os.listdir(path + sait_citi)
count_sait = list(filter(lambda x: x.endswith('.html'), files))
print("count_sait", count_sait)
num_page_old = len(count_sait)  # кол-во скачанных страниц, из к-х нужно доставать ссылки
print(num_page_old)
# num_page_old = 75


#for i in range(0, num_page_old):
#    name = sait + str(i) + '.html'
#    obj.download_links(name_file=name, name_tag='a', name_class='catalog-product__name')

for i in range(0, num_page_old):
    name = sait_citi + str(i) + '.html'
    obj_citi.download_links(name_file=name, name_tag='a', name_class='XD')

# print(len(unic_url))
# obj.download_unic_pages()
print("download_unic_pages - good")

import Class_Timer

# if (num_page_old==163783):
t1 = Class_Timer.Timer()
# DataBase = pd.DataFrame()

t1.start()
# files = os.listdir(path + sait + '_unic')
# count_sait_unic = list(filter(lambda x: x.endswith('.html'), files))

# for i in range(0, len(count_sait_unic)):
"""


"""
for i in range(0, 1350):
    name = 'dns_unic_' + str(i) + '.html'
    with open('C:\\Users\\Ingvar\\Desktop\\Documents\\WEB\\dns_unic\\' + name, 'r', encoding="utf-8") as html_file:
        tree_phone_charact = BeautifulSoup(html_file, "lxml")
        DataBase = collections_title_value(tree_phone_charact, DataBase, "")
print("Kol-vo phone", len(DataBase.index))
DataBase.to_feather("DataBase.feather")
t1.stop()
"""
