# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     got_house_info
   Description: 
   Author:        nxa28190
   Date:          7/5/2020
-------------------------------------------------
   Change Activity:
                  7/5/2020:
-------------------------------------------------
"""
__author__ = 'Richard Xiong'

import requests
import time
import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from lxml import etree
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.styles.colors import YELLOW
from datetime import datetime


class ExcelOper(object):
    def __init__(self):
        self.wb = Workbook()
        self.rename_first_sheet()

    def rename_first_sheet(self):
        # set the first default sheet name as Summary
        first_sheet = self.wb.active
        first_sheet.title = 'First'

    def create_sheet(self, name, index=None):
        self.wb.create_sheet(title=name, index=index)

    def set_value(self, sheet_name, row, column, value, color):
        # self.create_sheet(sheet_name)
        ws = self.wb[sheet_name]
        # ws.cell(row=row, column=column).value = value
        ws['{}{}'.format(column, row)].value = value

        # set alignment
        align = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws['{}{}'.format(column, row)].alignment = align

        # set backend color
        if color == 'green':
            fill = PatternFill("solid", fgColor='66cc33')
        elif color == 'grey':
            fill = PatternFill("solid", fgColor='cccccc')
        elif color == 'yellow':
            fill = PatternFill("solid", fgColor=YELLOW)
        ws['{}{}'.format(column, row)].fill = fill

        return ws

    def set_column_width(self, sheet_name, length, column='B'):
        ws = self.wb.get_sheet_by_name(sheet_name)
        ws.column_dimensions[column].width = length
        return ws

    def set_alignment(self, sheet_name, row, column, hstyle='center', vstyle='center', wrap_text=True):
        ws = self.wb.get_sheet_by_name(sheet_name)
        align = Alignment(horizontal=hstyle, vertical=vstyle, wrap_text=wrap_text)
        ws['{}{}'.format(column, row)].alignment = align
        return ws

    def set_font(self, sheet_name, row, column, name='Calibri', bold=False, color='FF000000'):
        ws = self.wb.get_sheet_by_name(sheet_name)
        font = Font(name=name, bold=bold, color=color)
        ws.cell(row=row, column=column).font = font
        return ws

    def set_hyper_link(self, sheet_name, row, column, hyper_sheet_name):
        ws = self.wb.get_sheet_by_name(sheet_name)
        ws.cell(row=row, column=column).value = hyper_sheet_name
        ws.cell(row=row, column=column).hyperlink = '#{}!A1'.format(hyper_sheet_name)
        return ws

    def active_sheet(self, sheet_name):
        ws = self.wb.get_sheet_by_name(sheet_name)
        return ws

    def save_wb(self, excel_name):
        self.wb.save(excel_name)


class HouseInfo(ExcelOper):
    def __init__(self, project, region):
        self.chrome = webdriver.Chrome()
        # self.chrome = webdriver.Ie()
        super(HouseInfo, self).__init__()

        self.chrome.get(BASE_URL)
        # input house info
        self.chrome.find_element_by_xpath('// *[ @ id = "ctl00_MainContent_txt_Pro"]').send_keys(project)

        # select region
        house_select = Select(self.chrome.find_element_by_id('ctl00_MainContent_ddl_RD_CODE'))
        house_select.select_by_value(region)
        # click search button
        self.chrome.find_element_by_xpath('//*[@id="ctl00_MainContent_bt_select"]').click()

    def get_house_set_lnk(self):
        # got the url link to count the house set number
        page_tree = etree.HTML(house.chrome.page_source)
        house_set = page_tree.xpath('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/child::tr/child::*/a/@href')
        house_set_link = []
        for i in range(1, len(house_set) + 1, 1):
            house_set_link.append('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[{}]/td/a'.format(i + 1))
        return house_set_link

    def enter_house_set(self, url):
        # enter first house set
        self.chrome.find_element_by_xpath(url).click()
        time.sleep(0.5)

    def get_house_link(self):
        # got the url link to count the house set number
        page_tree = etree.HTML(house.chrome.page_source)
        building_no = page_tree.xpath('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/child::tr/child::*/a/text()')
        print(building_no)
        house_link = []
        for i in range(1, len(building_no)+1, 1):
            house_link.append('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[{}]/td/a'.format(i + 1))
        # add all the build number and link to a list
        building_info = []
        for no, link in zip(building_no, house_link):
            info = {
                'number': no,
                'link': link
            }
            building_info.append(info)
        return building_info

    def back(self):
        self.chrome.back()

    def enter_house_info_page(self, house_link):
        # enter house derailed information page
        self.chrome.find_element_by_xpath(house_link).click()
        time.sleep(0.5)

        # got the house color and number
        page_tree = etree.HTML(self.chrome.page_source)
        house_no = page_tree.xpath('//*[@id="ctl00_MainContent_gvxml"]/tbody/child::tr/child::*/text()')
        house_color = page_tree.xpath('//*[@id="ctl00_MainContent_gvxml"]/tbody/child::tr/child::*/@style')

        print(house_color)
        print(house_no)

        for item in house_no[:]:
            if ('\xa0' == item) or ('地下车库' == item):
                print(item)
                house_no.remove(item)

        for item in house_color[:]:
            if ('background-color:White;' == item):
                print(item)
                house_color.remove(item)

        house_info = []
        for number, color in zip(house_no, house_color):
            info = {
                'number': number,
                'color': color
            }
            house_info.append(info)

        # remove the blank house information
        not_sale = 0
        for item in house_info:
            # if (('\xa0' or '地下车库') in item['number']) or ('background-color:White;' in item['color']):
            #     print(item)
            #     house_info.remove(item)
            if 'background-color:#66cc33;' in item['color']:
                not_sale = not_sale + 1

        all_house = len(house_info)
        sale_rate = (all_house - not_sale)/all_house

        print(house_color, house_no)
        print(house_info)
        print(not_sale)
        print(all_house)
        print(sale_rate)

        self.chrome.back()
        return not_sale, all_house, sale_rate, house_info


if __name__ == '__main__':
    COLUM_VALUE = ['A', 'B', 'C', 'D', 'E']
    COLOR = {'background-color:#66cc33;': 'green', 'background-color:#cccccc;': 'grey',
             'background-color:Yellow;': 'yellow'}
    BASE_URL = r'http://spf.szfcweb.com/szfcweb/(S(wwkvmt45ppfml2mkbrlotu35))/DataSerach/SaleInfoProListIndex.aspx'
    HOUSE_SET1 = '//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[1]/a'
    HOUSE_SET2 = '//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[3]/td[1]/a'
    HOUSE_SET3 = '//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[4]/td[1]/a'

    HOUSE_7_LINK = (7, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[1]/a')
    HOUSE_5_LINK = (5, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[3]/td[1]/a')
    HOUSE_9_LINK = (9, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[4]/td[1]/a')
    HOUSE_8_LINK = (8, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[5]/td[1]/a')
    HOUSE_LINK1 = [HOUSE_7_LINK, HOUSE_5_LINK, HOUSE_9_LINK, HOUSE_8_LINK]

    HOUSE_2_LINK = (2, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[1]/a')
    HOUSE_1_LINK = (1, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[3]/td[1]/a')
    HOUSE_6_LINK = (6, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[4]/td[1]/a')
    HOUSE_3_LINK = (3, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[5]/td[1]/a')
    HOUSE_4_LINK = (4, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[6]/td[1]/a')
    HOUSE_LINK2 = [HOUSE_2_LINK, HOUSE_1_LINK, HOUSE_6_LINK, HOUSE_3_LINK, HOUSE_4_LINK]

    HOUSE_10_LINK = (10, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[1]/a')
    HOUSE_11_LINK = (11, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[3]/td[1]/a')
    HOUSE_12_LINK = (12, r'//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[4]/td[1]/a')
    HOUSE_LINK3 = [HOUSE_10_LINK, HOUSE_11_LINK, HOUSE_12_LINK]

    # if not (len(sys.argv) == 3):
    #     print('Please input porject name and region')
    #     assert 0

    house = HouseInfo(sys.argv[1], sys.argv[2])
    # house = HouseInfo('都会', '吴中区')
    # house_set_link = house.get_house_set_lnk()
    for house_set_link in house.get_house_set_lnk():
        house.chrome.find_element_by_xpath(house_set_link).click()
        for building in house.get_house_link():
            # house.chrome.find_element_by_xpath(building['link']).click()

            house.create_sheet(str(building['number']))
            not_sale, all_house, sale_rate, house_info = house.enter_house_info_page(building['link'])
            for number, info in enumerate(house_info):
                row_value = int(number / 4 + 1)
                colum_value = number % 4
                house.set_value(sheet_name=str(building['number']), row=row_value, column=COLUM_VALUE[colum_value],
                                value=info['number'], color=COLOR[info['color']])

            house.set_value(sheet_name=str(building['number']), row=1, column='F', value='去化率', color='green')
            house.set_value(sheet_name=str(building['number']), row=2, column='F', value=sale_rate, color='green')
            house.set_value(sheet_name=str(building['number']), row=4, column='F', value='未售', color='green')
            house.set_value(sheet_name=str(building['number']), row=5, column='F', value=not_sale, color='green')
            house.set_value(sheet_name=str(building['number']), row=4, column='G', value='总量', color='green')
            house.set_value(sheet_name=str(building['number']), row=5, column='G', value=all_house, color='green')

        house.back()

        excel_name = '{}_{}_房屋销售统计{}.xlsx'.format(sys.argv[1], sys.argv[2], datetime.now().strftime('%y_%m_%d-%H-%M'))
        print(excel_name)
        house.save_wb(excel_name)

        # house.back()

    # got the url link to count the house set number
    # page_tree = etree.HTML(house.chrome.page_source)
    # house_set = page_tree.xpath('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/child::tr/child::*/a/@href')
    # for i in range(1, len(house_set)+1, 1):
    #     house.chrome.find_element_by_xpath('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[{}]/td/a'.format(i+1)).click()
    #     house.back()

    # house.chrome.get( "SaleInfoBudingShow.aspx?SPJ_ID=8e493585-89a4-4906-9f7d-cf46071ebab5")

    # url_pre = house.chrome.find_element_by_xpath('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[2]/td[1]/a')
    # print(url_pre)
    # print(url_pre.get_attribute('href'))
    # house.chrome.get(url_pre.get_attribute('href'))

    # house.enter_house_set(HOUSE_SET1)
    # for item in HOUSE_LINK1:
    #     house.create_sheet(str(item[0]))
    #     not_sale, all_house, sale_rate, house_info = house.enter_house_info_page(item[1])
    #     for number, info in enumerate(house_info):
    #         row_value = int(number / 4 + 1)
    #         colum_value = number % 4
    #         house.set_value(sheet_name=str(item[0]), row=row_value, column=COLUM_VALUE[colum_value],
    #                         value=info['number'], color=COLOR[info['color']])
    #
    #     house.set_value(sheet_name=str(item[0]), row=1, column='F', value='去化率', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=2, column='F', value=sale_rate, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='F', value='未售', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='F', value=not_sale, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='G', value='总量', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='G', value=all_house, color='green')
    #
    # house.back()






    # // *[ @ id = "ctl00_MainContent_OraclePager1"] / tbody / tr[2] / td[1] / a




    # for i in range(2,5,1):
    #     house.chrome.find_element_by_xpath('//*[@id="ctl00_MainContent_OraclePager1"]/tbody/tr[{}]/td/a[text()="熙筑"]'.format(i)).click()
    #     house.back()


    # house_set = house.chrome.find_element_by_link_text('都会上品花园')
    # house_set = house.chrome.find_element_by_xpath('// *[ @ id = "ctl00_MainContent_OraclePager1"] / tbody/tr/td/a')
    # print(house_set)
    # for link in house_set:
    #     print(link.get_attribute('href'))
    #     house.chrome.get(link.get_attribute('href'))

    # // *[ @ id = "ctl00_MainContent_OraclePager1"] / tbody/tr/td/a




    # house.enter_house_set(HOUSE_SET1)
    # for item in HOUSE_LINK1:
    #     house.create_sheet(str(item[0]))
    #     not_sale, all_house, sale_rate, house_info = house.enter_house_info_page(item[1])
    #     for number, info in enumerate(house_info):
    #         row_value = int(number / 4 + 1)
    #         colum_value = number % 4
    #         house.set_value(sheet_name=str(item[0]), row=row_value, column=COLUM_VALUE[colum_value],
    #                         value=info['number'], color=COLOR[info['color']])
    #
    #     house.set_value(sheet_name=str(item[0]), row=1, column='F', value='去化率', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=2, column='F', value=sale_rate, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='F', value='未售', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='F', value=not_sale, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='G', value='总量', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='G', value=all_house, color='green')
    #
    # house.back()
    #
    # house.enter_house_set(HOUSE_SET2)
    # for item in HOUSE_LINK2:
    #     house.create_sheet(str(item[0]))
    #     not_sale, all_house, sale_rate, house_info = house.enter_house_info_page(item[1])
    #     for number, info in enumerate(house_info):
    #         row_value = int(number / 4 + 1)
    #         colum_value = number % 4
    #         house.set_value(sheet_name=str(item[0]), row=row_value, column=COLUM_VALUE[colum_value],
    #                         value=info['number'], color=COLOR[info['color']])
    #
    #     house.set_value(sheet_name=str(item[0]), row=1, column='F', value='去化率', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=2, column='F', value=sale_rate, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='F', value='未售', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='F', value=not_sale, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='G', value='总量', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='G', value=all_house, color='green')
    # house.back()
    #
    # house.enter_house_set(HOUSE_SET3)
    # for item in HOUSE_LINK3:
    #     house.create_sheet(str(item[0]))
    #     not_sale, all_house, sale_rate, house_info = house.enter_house_info_page(item[1])
    #     for number, info in enumerate(house_info):
    #         row_value = int(number / 4 + 1)
    #         colum_value = number % 4
    #         house.set_value(sheet_name=str(item[0]), row=row_value, column=COLUM_VALUE[colum_value],
    #                         value=info['number'], color=COLOR[info['color']])
    #
    #     house.set_value(sheet_name=str(item[0]), row=1, column='F', value='去化率', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=2, column='F', value=sale_rate, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='F', value='未售', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='F', value=not_sale, color='green')
    #     house.set_value(sheet_name=str(item[0]), row=4, column='G', value='总量', color='green')
    #     house.set_value(sheet_name=str(item[0]), row=5, column='G', value=all_house, color='green')
    # house.back()
    #
    # excel_name = '{}.xlsx'.format(datetime.now().strftime('%y_%m_%d-%H-%M'))
    # print(excel_name)
    # house.save_wb(excel_name)

    # a = ['1', '2', '3', '地下车库','地下车库','\xa0', '\xa0', '\xa0']
    # print(a)
    # # for item in a:
    # #     print(item)
    # #     if ('地下车库' == item):
    # #         a.remove(item)
    # #     if ('\xa0' == item):
    # #         a.remove(item)
    # print(len(a))
    #
    # for i in range(0,len(a),1):
    #     print(i, a[i])
    #     if ('地下车库' == a[i]):
    #         a.remove(a[i])
    #     if ('\xa0' == a[i]):
    #         a.remove(a[i])

    # print(a)

    # for item in HOUSE_LINK:
    #     print(item[0])
    #     print(item[1])

    # house = HouseInfo()
    # house.enter_house_info_page(BASE_URL)

    # excel = ExcelOper()
    # excel.set_value('First', 2, 'B', 30, 'yellow')
    # excel.set_value('First', 3, 'B', 30, 'grey')
    # excel.set_value('First', 4, 'B', 30, 'green')
    #
    # excel.save_wb('test.xlsx')

    # from selenium import webdriver
    # from selenium.webdriver.support.select import Select
    # from time import sleep
    #
    # driver = webdriver.Chrome()
    # driver.implicitly_wait(10)
    # driver.get('http://www.baidu.com')
    # sel = driver.find_element_by_xpath("//select[@id='nr']")
    # Select(sel).select_by_value('50')  # 显示50条

    # import time
    # from selenium import webdriver
    #
    # '''
    # 测试用例：打开百度首页，搜索“胡歌”，然后检索列表，有无“胡歌的新浪微博”这个链接
    # 场景拆分：
    #     1）启动Chrome浏览器
    #     2) 打开百度首页，https://www.baidu.com
    #     3）定位搜索输入框，输入框元素XPath表达式：//*[@id="kw"]
    #     4）定位搜索提交按钮（百度一下）：//*[@id="su"]
    #     5）在搜索框输入“胡歌”，点击百度一下按钮
    #     6）在搜索结果列表判断是否存在“胡歌的新浪微博”这个链接
    #     7）退出浏览器，结束测试
    # '''
    # driver = webdriver.Chrome()
    # # driver.maximize_window()
    # # driver.implicitly_wait(8)  # 设置隐式等待时间
    #
    # driver.get("https://www.baidu.com")  # 地址栏里输入网址
    # driver.find_element_by_xpath('//*[@id="kw"]').send_keys("胡歌")  # 搜索框输入胡歌
    # driver.find_element_by_xpath('//*[@id="su"]').click()  # 点击百度一下按钮
    #
    # time.sleep(2)  # 等待2秒
    # # 通过元素XPath来确定该元素是否显示在结果列表，从而判断“壁纸”这个链接是否显示在结果列表
    # # find_element_by_link_text当找不到此链接时报错，程序停止
    # # driver.find_element_by_link_text('胡歌(中国内地男演员、歌手)_百度百科').is_displayed()
    # driver.find_element_by_xpath('//*[@id="1"]/h3/a').is_displayed()
    # driver.quit()
