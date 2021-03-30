# 修改mongo数据
# 去除 手续费的 \n
# 读取时间添加weekly
from quant_all.database.mongoData import get_collection
from datetime import date, timedelta


def update_add(collection_name):
    """
    weekday 添加
    :return:
    """
    for i in range(370,1460,1):
        day = date.today() - timedelta(days=i)
        print("正在调整",day)
        get_collection(collection_name).update_many({"日期": str(day)}, {"$set": {"weekday": str(day.weekday())}})
    print("添加星期几成功")


def get_all_fund_cod(collection_name):
    """
    获取基金的code
    :return:
    """
    vals = get_collection(collection_name).distinct("基金代码")
    for val in vals:
        in_val = get_collection(collection_name).find_one({"基金代码": val})
        item = {}
        item["基金代码"] = in_val["基金代码"]
        item["基金简称"] = in_val["基金简称"]
        try:
            get_collection("all_funds").insert_one(item)
        except Exception as e:
            print("出现异常", e)
    print("加载 所有基金 代号 成功")


def clean_data(collection_name):
    # 获取所有的手续费
    vals = get_collection(collection_name).distinct("日增长率")
    for val in vals:
        get_collection(collection_name).update_many({"日增长率": val}, {"$set": {"日增长率": val.strip()}})
    print("清理手续费中\\n")


if __name__ == '__main__':
    # clean_data('hostory_vals')
    update_add('hostory_vals')
    # get_all_fund_cod('hostory_vals')
    pass

