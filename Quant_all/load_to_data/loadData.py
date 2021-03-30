from quant_all.database.mongoData import databases


class loadData(object):

    def __init__(self):
        pass

    def load_to_mongo(self, field, file_name, collection_name):
        """
        file to mongo
        :param field:
        :param file_name:
        :param collection_name:
        :return:
        """
        fields = field.split(",")
        data = open(file_name, 'r', encoding='utf-8').readlines()
        for dat in data[1:]:
            vals = dat.split(",")
            item = dict(zip(fields, vals))
            databases[collection_name].insert_one(item)
        print("加载完成")


    def to_mongo(self,field, data, collection_name):
        """
        data to mongo
        :param field:
        :param data:
        :param collection_name:
        :return:
        """
        if isinstance(field, list):
            fields = field
        elif isinstance(field, str):
            fields = field.split(",")
        else:
            raise Exception("to_mongo field未知数据类型")
        item = dict(zip(fields, data))
        databases[collection_name].insert_one(item)
