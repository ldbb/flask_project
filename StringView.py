# 解决字符串在显示时的多余括号问题
import re

# 单个查询返回字典
def DictView(Dict):
    for key, value in Dict.items():
        if (key == 'title'):
            Str = Dict[key]
            Str_new = ""
            for i in range(len(Str)):  # 遍历标题字符串
                if ((Str[i] == "{") or (Str[i] == "}") or (Str[i] == "[") or (Str[i] == "]")):
                    continue
                Str_new = Str_new + Str[i]
            Dict[key] = Str_new
        if (key == 'author'):
            Str = Dict[key]
            Str_new = ""
            Str = re.sub(r"\\.", "", Str)  # 去除转义字符
            for i in range(len(Str)):  # 遍历标题字符串
                if ((Str[i] == "{") or (Str[i] == "}") or (Str[i] == "[") or (Str[i] == "]") or (Str[i] == "``")):
                    continue
                Str_new = Str_new + Str[i]
            Dict[key] = Str_new
        if (key == 'abstract'):
            Str = Dict[key]
            Str_new = ""
            Str = re.sub(r"\\.", "", Str)  # 去除转义字符
            for i in range(len(Str)):  # 遍历标题字符串
                if ((Str[i] == "{") or (Str[i] == "}") or (Str[i] == "[") or (Str[i] == "]")):
                    continue
                Str_new = Str_new + Str[i]
            Dict[key] = Str_new
    return Dict


# 多个查询返回数组
def StringView(*args):
    global List
    for List in args:  #第一层遍历，返回一个列表
        for Dict in List:  #第二层遍历，返回多个字典
            DictView(Dict)
    return List



