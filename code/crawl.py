# -*- coding: utf-8 -*-
import pandas as pd
import requests
from selenium import webdriver
import os 
import shutil
from tqdm import tqdm
shutil.rmtree('./data/',ignore_errors=True)
os.mkdir('./data/')


driver = webdriver.Chrome()
driver.get('https://foodlover.tw/lookup-shop.html')
ele_cat = driver.find_element_by_id('categoryOption')
cat_l = []
for a in ele_cat.find_elements_by_css_selector("*"):
    if 'none' in a.get_attribute('style'):
        pass
    else :
        print(a.text,a.get_attribute('style'))
        cat_l.append(a.text)

ele_zone = driver.find_element_by_id('zoneOption')
area_l= []
for zone in ele_zone.find_elements_by_css_selector("*"):
    if 'none' not in zone.get_attribute('style'):
        print(zone.text,zone.get_attribute('style'))
        zone.click()
        ele_city = driver.find_element_by_id('cityOption')
        for city in ele_city.find_elements_by_css_selector("*"):
            if 'none' not in city.get_attribute('style'):
                print(city.text)
                city.click()
                ele_area= driver.find_element_by_id('areaOption')
                for area in ele_area.find_elements_by_css_selector("*"):
                    if '所有行政區' not in area.text:
                        area_l.append((zone.text,city.text,area.text))
driver.quit()                    


for category in cat_l:
    print(category)
    for zone,city,area in tqdm(area_l):
        url = f'https://foodlover.tw/goodfood/query/shop/v2?shop=&category={category}&zone={zone}&city={city}&area={area}'
        #&pay_tool=信用卡&pay_tool=行動支付&pay_tool=電子票證'
        res = requests.get(url)
        with open(f"./data/{category.replace('/','_')}_{city}_{area}.json",'w',encoding='utf8') as f:
            f.write(res.text)

