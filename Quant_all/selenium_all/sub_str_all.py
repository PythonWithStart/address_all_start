import re

def sub_titles(titles):
    # 替换title
    titles_str = "\t".join(titles)
    titles_str = re.sub("f2\t", "最新价\t", titles_str)
    titles_str = re.sub("f3\t", "涨跌幅\t", titles_str)
    titles_str = re.sub("f12\t", "转债代码\t", titles_str)
    titles_str = re.sub("f14\t", "转债名称\t", titles_str)
    titles_str = re.sub("f227", "纯债价值", titles_str)
    titles_str = re.sub("f229", "最新价/正股价格", titles_str)
    titles_str = re.sub("f227", "纯债价值", titles_str)
    titles_str = re.sub("f229", "最新价", titles_str)
    titles_str = re.sub("f230", "涨跌幅", titles_str)
    titles_str = re.sub("f232", "正股代码", titles_str)
    titles_str = re.sub("f234", "正股名称", titles_str)
    titles_str = re.sub("f236", "转股价值", titles_str)
    titles_str = re.sub("f238", "纯债溢价率", titles_str)
    titles_str = re.sub("f237", "转股溢价率", titles_str)
    titles_str = re.sub("f239", "回售触发价", titles_str)
    titles_str = re.sub("f240", "强赎触发价", titles_str)
    titles_str = re.sub("f241", "到期赎回价", titles_str)
    titles_str = re.sub("f242", "开始转股日", titles_str)
    titles_str = re.sub("f243", "申购日期", titles_str)
    titles_str = re.sub("f116\t", "总市值\t", titles_str)
    # titles_str = re.sub("MRTYDATE\t", "到期日期", titles_str)
    titles_str = re.sub("LASTVALUEDATE\t", "到期日期", titles_str)
    titles = titles_str.split("\t")
    return titles