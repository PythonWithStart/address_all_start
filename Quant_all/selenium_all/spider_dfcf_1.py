import requests
import json
import openpyxl
from datetime import datetime
from sub_str_all import sub_titles

tries = 5
delay = 5
backoff = 5

pages = 8
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}


class spiderStart(object):

    url_base_format = "http://36.push2.eastmoney.com/api/qt/clist/get?" \
        "cb=" \
        "&pn={}" \
        "&pz=50" \
        "&po=1" \
        "&np=1" \
        "&ut=bd1d9ddb04089700cf9c27f6f7426281" \
        "&fltt=2" \
        "&invt=2" \
        "&fid=f243" \
        "&fs=b:MK0354" \
        "&fields=f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243,f116" \
        "&_=1611665316901"

    url_real_format = "http://push2.eastmoney.com/api/qt/stock/get?" \
          "invt=2&" \
          "fltt=2&" \
          "fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f260,f261,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292,f293,f181,f294,f295,f279,f288" \
          "&secid=0.{}" \
          "&cb=" \
          "&_=1611845797702"

    url_code_format = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js?" \
          "type=ZQ_JBXX&" \
          "token=70f12f2f4f091e459a279469fe49eca5&" \
          "callback=&" \
          "filter=(BONDCODE%3D%{}%27)(TEXCH%3D%27CNSESZ%27)&" \
          "_=1611848174762:formatted"


    def __init__(self):
        pass

    def get_response(self, url, headers):
        return requests.get(url, headers=headers)

    def get_title_vals(self, resp, resp_dict_str='data.diff'):
        titles = []
        # all_vals = []
        for index, dat in enumerate(self.resp_json_dict(resp, resp_dict_str)):
            if index == 0:
                titles.extend([key for key, values in dat.items()])
            vals = [values for key, values in dat.items()]
            # all_vals.append(vals)
            yield titles, vals
        # return titles, all_vals

    def get_real_vals(self, resp, resp_dict_str='data'):
        data = self.resp_json_dict(resp, resp_dict_str)
        titles = []
        all_vals = []
        titles.extend([key for key, values in data.items()])
        vals = [values for key, values in data.items()]
        titles = sub_titles(titles)
        ntitles = filter_data(titles, titles)
        nvals = filter_data(titles, vals)
        all_vals.extend(nvals)
        return need_dict(to_dict(ntitles, all_vals), ["总市值"])

    def get_time_msg(self, resp, resp_dict_str=''):
        data = self.resp_json_dict(resp, resp_dict_str)[0]
        titles = []
        all_vals = []
        titles.extend([key for key, values in data.items()])
        vals = [values for key, values in data.items()]
        titles = sub_titles(titles)
        ntitles = filter_data(titles, titles)
        nvals = filter_data(titles, vals)
        all_vals.extend(nvals)
        return need_dict(to_dict(ntitles, all_vals), ["到期日期"])

    def resp_json_dict(self, resp, keys=''):
        """
        :param resp:
        :param keys:
        :return:
        """
        ndict = json.loads(resp.text)
        for index, key in enumerate(keys.split(".")):
            vndict = ndict.get(key)
            if vndict is None:
                return ndict
            else:
                ndict = vndict
        return ndict

    def run(self):
        page = 1
        resp = self.get_response(url=self.url_base_format.format(page), headers=headers)
        for dat in self.get_title_vals(resp, "data.diff"):
            # 获取正股信息
            stock_code = dat[1][8]
            resp = self.get_response(url=self.url_real_format.format(stock_code), headers=headers)
            stock_val = self.get_title_vals(resp, "data")
            print(next(stock_val))
            # 获取债券到期日期
            # 获取 可转债详细数据
            convertible_bond_code = dat[1][2]
            resp = self.get_response(url=self.url_code_format.format(convertible_bond_code), headers=headers)
            convertible_val = self.get_title_vals(resp, '')
            # print(convertible_val)
            print(next(convertible_val))
            # print(dat)



def get_page_data(page=1):
    url = "http://36.push2.eastmoney.com/api/qt/clist/get?" \
          "cb=" \
          f"&pn={page}" \
          "&pz=50" \
          "&po=1" \
          "&np=1" \
          "&ut=bd1d9ddb04089700cf9c27f6f7426281" \
          "&fltt=2" \
          "&invt=2" \
          "&fid=f243" \
          "&fs=b:MK0354" \
          "&fields=f1,f152,f2,f3,f12,f13,f14,f227,f228,f229,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f26,f243,f116" \
          "&_=1611665316901"

    resp = requests.get(url, headers=headers)
    titles = []
    all_vals = []
    for index, dat in enumerate(json.loads(resp.text)["data"]["diff"]):
        if index == 0:
            titles.extend([key for key, values in dat.items()])
        vals = [values for key, values in dat.items()]
        all_vals.append(vals)
    return titles, all_vals


def get_real_msg(fundcode):
    # 获取正股信息
    url = "http://push2.eastmoney.com/api/qt/stock/get?" \
          "invt=2&" \
          "fltt=2&" \
          "fields=f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f260,f261,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292,f293,f181,f294,f295,f279,f288" \
          f"&secid=0.{fundcode}" \
          "&cb=" \
          "&_=1611845797702"
    # print("当前 [正股信息] 所有的url", url)
    resp = requests.get(url, headers=headers)
    titles = []
    all_vals = []
    data = json.loads(resp.text)["data"]
    if data is None:
        return {}
    titles.extend([key for key, values in data.items()])
    vals = [values for key, values in data.items()]
    titles = sub_titles(titles)
    ntitles = filter_data(titles, titles)
    nvals = filter_data(titles, vals)
    all_vals.extend(nvals)
    return need_dict(to_dict(ntitles, all_vals), ["总市值"])


def get_time_msg(fundcode):
    url = "http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js?" \
          "type=ZQ_JBXX&" \
          "token=70f12f2f4f091e459a279469fe49eca5&" \
          "callback=&" \
          f"filter=(BONDCODE%3D%{fundcode}%27)(TEXCH%3D%27CNSESZ%27)&" \
          "_=1611848174762:formatted"

    # print("当前 [到期日期] 所有的url", url)
    resp = requests.get(url, headers=headers)
    titles = []
    all_vals = []
    data = json.loads(resp.text)[0]
    titles.extend([key for key, values in data.items()])
    vals = [values for key, values in data.items()]
    titles = sub_titles(titles)
    ntitles = filter_data(titles, titles)
    nvals = filter_data(titles, vals)
    all_vals.extend(nvals)
    return need_dict(to_dict(ntitles, all_vals), ["到期日期"])


def to_dict(title="", vals=''):
    if title == '':
        return {}
    return {v: vals[index] for index, v in enumerate(title)}


def need_dict(item, keys=[]):
    if item == {}:
        return {}
    return {key: val for key, val in item.items() if key in keys}


def filter_data(titles, data):
    need_vals = [title.startswith("f") for title in titles]
    data = [dat for index, dat in enumerate(data) if need_vals[index] is False]
    return data


def load_data_excel():
    time_str = datetime.strftime(datetime.now(), "%Y_%m_%d")
    titles, all_vals = get_page_data()
    titles = sub_titles(titles)
    book = openpyxl.Workbook()
    sheet = book.active
    ntitles = filter_data(titles, titles)
    print(ntitles)
    all_vals.insert(0, ntitles)
    print("--90909--", all_vals[0])
    for index, row in enumerate(all_vals):
        if index == 0:
            print(type(row))
            row.extend(['到期日期', '总市值'])
            print(row)
            sheet.append(row)
            continue
        # print(row)
        row = filter_data(titles, row)
        # 获取 可转债详细数据
        convertible_bond_code = row[2]
        vgtet_time_msg = get_time_msg(convertible_bond_code)
        print("vgtet_time_msg", vgtet_time_msg)
        # 获取 股票详细数据
        stock_code = row[8]
        vget_real_msg = get_real_msg(stock_code)
        print("vget_real_msg", vget_real_msg)
        print("----a", row)
        row.extend([vgtet_time_msg.get('到期日期', ''), vget_real_msg.get("总市值", "")])
        sheet.append(row)

    for i in range(2, 9, 1):
        # 获取数据
        _, all_vals = get_page_data(i)
        for row in all_vals:
            print("---->", row)
            # print(row)
            row = filter_data(titles, row)
            # 获取 可转债详细数据
            convertible_bond_code = row[2]
            vgtet_time_msg = get_time_msg(convertible_bond_code)
            print("vgtet_time_msg", vgtet_time_msg)
            # 获取 股票详细数据
            stock_code = row[8]
            vget_real_msg = get_real_msg(stock_code)
            print("vget_real_msg", vget_real_msg)
            print("----a", row)
            row.extend([vgtet_time_msg.get('到期日期', ''), vget_real_msg.get("总市值", "")])
            sheet.append(row)
    file_name = f'appending_{time_str}.xlsx'
    print(file_name)
    book.save(file_name)


if __name__ == '__main__':
    obj = spiderStart()
    obj.run()
    # load_data_excel()
    # titles, all_vals = get_time_msg()
    # print(titles)
