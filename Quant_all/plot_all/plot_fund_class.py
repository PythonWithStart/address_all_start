# coding ='utf-8'
import pymongo
from pylab import mpl
import matplotlib.pyplot as plt
from quant_all.database.mongoData import get_collection

# 基本设置
mpl.rcParams['font.sans-serif'] = ['SimHei']


class getData(object):
    def get_data(self, fund_code="", is_all=False):
        # 获取基金
        if is_all is False:
            if fund_code == "":
                vals = get_collection("all_funds").find_one({})
            else:
                vals = get_collection('all_funds').find_one({'基金代码': fund_code})
            return vals
        else:
            vals = get_collection("all_funds").find()
            return vals

    def get_data_to_show(self, vals, isdel_error=True):
        # print(vals['基金代码'])
        all_vals = get_collection("hostory_vals").find({"基金代码": vals['基金代码']}).sort([('日期', pymongo.ASCENDING)])
        items = []
        for all_val in all_vals:
            if all_val['weekday'] == '2' or all_val['weekday'] == '3' or all_val['weekday'] == '4':
                if all_val['weekday'] == '2':
                    item = {}
                    item["start"] = "\t".join([all_val['日期'], all_val['单位净值'], all_val['weekday']])
                elif all_val['weekday'] == '3':
                    item["middle"] = "\t".join([all_val['日期'], all_val['单位净值'], all_val['weekday']])
                elif all_val['weekday'] == '4':
                    item["end"] = "\t".join([all_val['日期'], all_val['单位净值'], all_val['weekday']])
                    items.append(item)
        if isdel_error:
            # 删除 不符号要求的数据
            self.del_index_item(items)
        else:
            # 改变 不符合要求的数据
            self.exchange_items(items)
        # 获取三组数据
        three_vals = [[], [], [], []]
        for item in items:
            three_vals[0].append(item["middle"].split("\t")[0])
            three_vals[1].append(float(item["start"].split("\t")[1]))
            three_vals[2].append(float(item["middle"].split("\t")[1]))
            three_vals[3].append(float(item["end"].split("\t")[1]))
        print(three_vals)
        return three_vals, vals

    @staticmethod
    def del_index_item(items):
        # 剔除不符合要求的数据
        # todo 需要检查下日期 日期不连续的但是星期连续的数据 也要删除
        del_index = []
        for index, item in enumerate(items):
            if item.get("start") is not None and item.get("middle") is not None and item.get('end') is not None:
                pass
            else:
                del_index.append(index)
        for i in del_index:
            print("需要删除的", i)
            del items[i]
        print(items)
        return items

    @staticmethod
    def exchange_items(items):
        # 修正参数
        # # 修正参数
        # for index, item in enumerate(items):
        #     # 日期检查
        #     current_check_day = item
        return items

    def run_test(self):
        vals = self.get_data()
        return self.get_data_to_show(vals)

    def run_one(self, fund_code='000006'):
        vals = self.get_data(fund_code)
        return self.get_data_to_show(vals)

    def run_more(self, fund_codes=[]):
        for fund_code in fund_codes:
            vals = self.get_data(fund_code)
            yield self.get_data_to_show(vals)

    def run_all(self):
        vals = self.get_data(is_all=True)
        for val in vals:
            yield self.get_data_to_show(val)


class plot(object):


    def __init__(self, data, title, xlabel, ylabel, colour=['b-', 'r-', 'g-'], rotation=45):
        self.data = data
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.rotation = rotation
        self.colour = colour

    def plot(self):
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.xlabel)
        plt.xticks(rotation=self.rotation)

        if len(self.data) - 1 != len(self.colour):
            print("colour 和 数据不匹配 将优先采用最短策略")
        endlen = min(len(self.data) - 1, len(self.colour))
        start_data = []
        for i in range(endlen):
            start_data.append(self.data[0])
            start_data.append(self.data[i + 1])
            start_data.append(self.colour[i])
        plt.plot(*start_data)
        plt.grid()
        plt.show()


if __name__ == '__main__':
    # three_vals, vals = get_data()
    gda = getData()
    three_vals, vals = gda.run_one(fund_code='001951')
    # print(three_vals)
    onePlot = plot(three_vals, f"当前基金-{vals['基金代码']}--{vals['基金简称']}", "日期", '基金净值变化')
    onePlot.plot()
