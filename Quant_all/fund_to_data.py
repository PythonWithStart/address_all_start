# -*-coding:utf-8 -*-
import re
import csv
import time
import requests
import pandas as pd
from load_to_data.loadData import loadData


class fundSpider(object):
    ldata = loadData

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Referer': 'http://fund.eastmoney.com/data/fundranking.html'}
        self.listPagePath = "列表页.csv"
        self.historyPath = "历史净值明细.csv"
        self.industryPath = "行业.csv"

    def listPage(self):  # 列表页
        title = ["基金代码", "基金简称", "日期", "单位净值", "累计净值", "日增长率", "近1周", "近1月", "近3月", "近6月", "近1年", "近2年", "近3年", "今年来",
                 "成立以来", "手续费"]
        ed = str(time.strftime("%Y-%m-%d"))  # 今天的时间
        for pi in range(1, 123):
            url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd={}&ed={}&qdii=&tabSubtype=,,,,,&pi={}&pn=50&dx=1".format(
                ed, ed, str(pi))
            res = requests.get(url=url, headers=self.headers, timeout=10).content.decode()
            print(res)
            data_list = re.findall(r'"(.*?)"', res, re.S)
            for data in data_list:
                item_list = re.findall(r'(.*?),', data, re.S)
                for num in [2, 15, 15, 15, 15]:
                    del item_list[num]
                for i in range(0, 3):
                    item_list.pop()
                print(pi, item_list)
                self.ldata().to_mongo(title, item_list, "page_vals")

    def history(self):  # 历史净值明细
        title = ["基金代码", "基金简称", "日期", "单位净值", "累计净值", "日增长率"]
        df = pd.read_csv(self.listPagePath, encoding="utf-8", dtype={"基金代码": str})
        source_list = df.values.tolist()
        y = 0
        for source in source_list:
            y += 1
            url = "http://api.fund.eastmoney.com/f10/lsjz?fundCode={}&pageIndex=1&pageSize=200".format(source[0])
            res = requests.get(url=url, headers=self.headers, timeout=10).content.decode()
            data_list = re.findall(r'"(.*?)"', res, re.S)
            num = 0
            for data in data_list:
                num += 1
                if data == "FSRQ":
                    day_growth = data_list[num + 11]  # 日增长率
                    if day_growth == "FHFCZ":
                        day_growth = data_list[num + 6]
                    item = [source[0], source[1], data_list[num], data_list[num + 2], data_list[num + 4], day_growth]
                    print(y, item)
                    self.ldata().to_mongo(self, title, item, "hostory_vals")

    def industry(self):  # 行业
        title = ["基金代码", "基金简称", "行业类别", "占净值比例", "市值（万元）"]
        df = pd.read_csv(self.listPagePath, encoding="utf-8", dtype={"基金代码": str})
        source_list = df.values.tolist()
        y = 0
        for source in source_list:
            y += 1
            self.headers["Referer"] = "http://fundf10.eastmoney.com/hytz_{}.html".format(source[0])
            url = "http://api.fund.eastmoney.com/f10/HYPZ/?fundCode={}&year=2020".format(source[0])
            res = requests.get(url=url, headers=self.headers, timeout=10).content.decode()
            print(res)
            HYMC = re.findall(r'"HYMC":"(.*?)"', res, re.S)  # 行业类别
            ZJZBL = re.findall(r'"ZJZBL":"(.*?)"', res, re.S)  # 占净值比例
            SZDesc = re.findall(r'"SZDesc":"(.*?)"', res, re.S)  # 市值（万元）
            num = 0
            for data in HYMC:
                item = [source[0], source[1], data, ZJZBL[num], SZDesc[num]]
                print(y, item)
                self.ldata().to_mongo(title, item, "industry_vals")
                num += 1


if __name__ == '__main__':
    obj = fundSpider()
    obj.listPage()  # 此方法每天执行
    # obj.history()  # 此方法只要执行一次就可以了，每天执行obj.listPage()已经有该数据了
    # obj.industry()  # 此方法一个月执行一次就可以了
