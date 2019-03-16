import itchat
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import numpy as np
import PIL.Image as Image
from os import path
from pyecharts import Pie
import csv
from pyecharts import Geo
from collections import Counter
from pyecharts import Bar


'''
作者：pk哥
公众号：Python知识圈
日期：2018/10/11
代码解析详见公众号「Python知识圈」。
'''


def get_info():
    itchat.auto_login()  # 登录微信
    friends = itchat.get_friends(update=True)[0:]    # 获取所有好友信息
    nickNames = []
    remarkNames = []
    sexs = []
    signatures = []
    provinces = []
    citys = []
    for i in friends:
        nickName = i['NickName'].strip().replace('span', '').replace('class', '').replace('emoji', '').replace('\n', '').replace('\"', '').replace('🤣', '')  # 去除无用字符
        remarkName = i['RemarkName'].strip().replace('span', '').replace('class', '').replace('emoji', '').replace('\n', '').replace('\"', '').replace('🤣', '')  # 去除无用字符
        sex = i['Sex']
        signature = i['Signature'].strip().replace('span', '').replace('class', '').replace('emoji', '').replace('\n', '').replace('\"', '')     # 去除无用字符
        rep = re.compile("1f\d+\w*|[<>/=]")
        signature = rep.sub('', signature)
        province = i['Province']
        city = i['City']
        nickNames.append(nickName)
        remarkNames.append(remarkName)
        sexs.append(sex)
        signatures.append(signature)
        provinces.append(province)
        citys.append(city)
    return zip(nickNames, remarkNames, sexs, signatures, provinces, citys)


def get_data():
    datas =[]
    data = get_info()
    for nn, rn, se, si, pr, ci in data:
        info = {}
        info['昵称'] = nn
        info['备注名称'] = rn
        info['性别'] = se
        info['个性签名'] = si
        info['省份'] = pr
        info['城市'] = ci
        datas.append(info)
    return datas


def write2csv(datas):
    print('正在保存数据')
    with open('微信好友信息收集.csv', 'a', newline='', encoding='utf-8-sig') as f:   # 文件默认保存在项目所在的目录
        fieldnames = ['昵称', '备注名称', '性别', '个性签名', '省份', '城市']  # 控制列的顺序
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(datas)
        print("微信好友csv文件保存成功,在项目代码目录下查看")


datas = get_data()
write2csv(datas)     # 调用函数保存 csv 文件

# 绘制性别饼形图
male = female = other = 0
for i in datas:
    sex = i['性别']
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1
gender = ['男', '女', '其他']
num = [male, female, other]
pie = Pie('微信好友性别比例饼图')
pie.add('', gender, num, is_label_show=True)
pie.render('E:\\pye\\gender.html')     # 在指定目录下生成一个 gender.html 的文件
print('性别饼形图完成，到保存的目录下打开即可查看')


# 绘制昵称词云图
nicklist = []
for j in datas:
    nickname = j['昵称']
    rep = re.compile("1f\d+\w*|[<>/=]")
    nickname = rep.sub('', nickname)
    nicklist.append(nickname)
text = "".join(nicklist)
cut = jieba.cut(text, cut_all=True)     # 分词
word = ",".join(cut)
coloring = np.array(Image.open("E:\\nick.jpg"))  # 电脑中自定义词云的图片
my_wordcloud = WordCloud(background_color="white", max_words=3000, max_font_size=200,
                         mask=coloring, random_state=100, font_path='./font/STXINGKA.TTF',
                         scale=2).generate(word)  # 定义词云背景图颜色、尺寸、字体大小、电脑中字体选择,random_state 为每个单词返回一个PIL颜色
image_colors = ImageColorGenerator(coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))  # 绘图颜色
plt.imshow(my_wordcloud)  # 绘图内容
plt.axis("off")
# plt.show()  # 显示图
d = path.dirname(__file__)  # project 当前目录
my_wordcloud.to_file(path.join(d, 'nickname.png'))
print('昵称词云图完成，在项目代码目录下查看')


# 绘制个性签名词云图
signlist = []
for k in datas:
    signature = k['个性签名']
    rep = re.compile("1f\d+\w*|[<>/=]")
    signature = rep.sub('', signature)
    signlist.append(signature)
text = "".join(signlist)
cut = jieba.cut(text, cut_all=True)     # 分词
word = ",".join(cut)
coloring = np.array(Image.open("E:\\sign.jpg"))  # 电脑中自定义词云的背景图片，需要事先自己准备好
my_wordcloud = WordCloud(background_color="white", max_words=3000, max_font_size=200,
                         mask=coloring, random_state=100, font_path='./font/STXINGKA.TTF',
                         scale=2).generate(word)  # 定义词云背景图颜色、尺寸、字体大小、电脑中字体选择,random_state 为每个单词返回一个PIL颜色
image_colors = ImageColorGenerator(coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))  # 绘图颜色
plt.imshow(my_wordcloud)  # 绘图内容
plt.axis("off")
# plt.show()  # 显示图
d = path.dirname(__file__)  # project 当前目录
my_wordcloud.to_file(path.join(d, 'sign.png'))
print('个性签名词云图完成，在项目代码目录下查看')


# 绘制微信好友地区分布图
citys = []
for h in datas:
    city = h['城市']
    citys.append(city)
cityss = filter(None, citys)       # 去除列表中空白字符，有些微信好友没填城市信息
res = Counter(cityss)
for key in list(res.keys()):
        if res.get(key) < 6:
            del res[key]

key = list(res.keys())
value = list(res.values())
bar = Bar("微信好友分布图")
# 用于添加图表的数据和设置各种配置项
# is_more_utils=True可以按右边的下载按钮将图片下载到本地

bar.add("地区分布图", key, value, is_more_utils=True, mark_line=["min", "max"],
        xaxis_rotate=45, is_label_show=True)
bar.show_config()  # 打印输出图表的所有配置项
bar.render('E:\\pye\\city.html')  # 在指定目录下生成一个 city.html 的文件
print('微信好友分布图完成，在项目代码目录下查看')

'''
作者：pk哥  
公众号：brucepk
日期：2018/10/11
代码解析详见公众号「brucepk」。

如有疑问或需转载，请联系微信号：dyw520520，备注来意，谢谢。
如需加入python技术交流群，请加我微信，备注「进群」，我拉你进群，一起讨论交流，共同成长。
'''
