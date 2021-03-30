from pymongo import MongoClient

connect = MongoClient("mongodb://localhost:27017")
databases = connect["quant_all"]


def load_to_mongo(field, file_name, collection_name):
    fields = field.split(",")
    data = open(file_name, 'r', encoding='utf-8').readlines()
    for dat in data[1:]:
        vals = dat.split(",")
        item = dict(zip(fields, vals))
        databases[collection_name].insert_one(item)
    print("加载完成")


if __name__ == '__main__':
    page_field = "基金代码,基金简称,日期,单位净值,累计净值,日增长率,近1周,近1月,近3月,近6月,近1年,近2年,近3年,今年来,成立以来,手续费"
    collection_name = 'page_vals'
    file_name = "列表页.csv"
    load_to_mongo(page_field, file_name, collection_name)

    page_field = "基金代码,基金简称,日期,单位净值,累计净值,日增长率"
    collection_name ='hostory_vals'
    file_name = "历史净值明细.csv"
    load_to_mongo(page_field, file_name, collection_name)

    page_field = "基金代码,基金简称,行业类别,占净值比例,市值（万元）"
    collection_name = 'industry_vals'
    file_name = "../行业.csv"

    load_to_mongo(page_field, file_name, collection_name)
