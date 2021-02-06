from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl


def get_html(page):
    # 调用chrome浏览器打开网页
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    request_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-' + str(page) + '.shtml'
    driver.get(request_url)
    time.sleep(1)
    #提取网页html信息
    html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    return html


def parse_table(content):
    # 用BS4解析html信息
    soup = BeautifulSoup(content, 'html.parser')
    # 定位表格位置
    tbody = soup.find('tbody')
    # 定位表头位置
    th_list = tbody.find_all('th')
    columns = []
    for th in th_list:
        columns.append(th.text)
    df = pd.DataFrame(columns=columns)
    # 定位表格的行
    tr_list = tbody.find_all('tr')
    for tr in tr_list:
        if tr_list.index(tr) == 0:
            continue
        # 定位每行的每列
        td_list = tr.find_all('td')
        temp = {}
        column_index = 0
        for td in td_list:
            temp[columns[column_index]] = td.text
            column_index += 1
        df = df.append(temp, ignore_index=True)
    return df


df_all = pd.DataFrame()
# 定义爬取页数
for i in range(3):
    if i == 0:
        continue
    content = get_html(i)
    df = parse_table(content)
    df_all = df_all.append(df)
print(df_all)
df_all.to_excel('车质网爬虫.xlsx', index=False)

