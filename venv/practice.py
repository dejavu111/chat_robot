import json
import requests
from requests.exceptions import RequestException
import re
import time
import webbrowser
import socket
'''
项目：聊天机器人助手   Author: dejavu111 
功能：
可以在控制台聊天
可以打开百度网页
可以打开新浪网页
可以爬取豆瓣热映电影
'''



#爬取豆瓣热映电影

#根据路径获取网页内容
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
#提取网页内容
def parse_one_page(html):
    # pattern = re.compile('<li class="ui-slide-item".*?>.*?<ul class="">.*?<li class="poster">.*?href="(.*?)".*?<img src="(.*?)".*?</a>.*?</li>.*?"title".*?<a.*?href=".*?".*?>(.*?)</a>.*?</li>.*?"rating".*?"subject-rate">(.*?)</span>.*?</li>.*?</ul>',re.S)
    # print(pattern)
    # pattern1 = re.compile('<li class="ui-slide-item.*?<ul class="">(.*?)</ul>')
    pattern1 = re.compile('<ul class="">(.*?)</ul>', re.S)
    # print(html)
    items = re.findall(pattern1, html)
    # print(items)
    pattern2 = re.compile('<li class="poster">.*?href="(.*?)".*?<img src="(.*?)".*?class="">(.*?)<.*?subject-rate">(.*?)</span>', re.S)
    l_t = []
    for item in items:
        # print(item)
        c_items = re.findall(pattern2, item)
        # print(c_items.__len__())
        if c_items.__len__()>0:
            l_t.append(c_items)

    # print(items)
    l = []
    for item1 in l_t:
        # print(item)
        item = item1[0]
        d = {
            'href': item[0],
            'img': item[1],
            'name': item[2],
            'score': item[3]
        }
        l.append(d)
    return l


#将内容写入文件
def write_to_file(index,content):
    # print(index)
    #f1 = "template/yemian-m3.html"
    f1 = "yemian.html"
    if index>0:
        f1 = "yemian.html"
    # f = open("yemian-m3.html","r")
    f = open(f1, "r")
    fc = f.read()
    pos = fc.find('<div class="movie_list">')
    # content = '<div><img src="img/'+str(index)+'.jpg"/>'+content["name"]+'</div>'
    content = '<img src="img/'+str(index)+'.jpg"/>'
    fc = fc[:pos]+content+fc[pos:]
    # fc = fc.replace('<div class="movie_list">', content)
    f = open("yemian.html","w")
    f.write(fc)
    f.close()


#保存图片到本地
def write_img(index,src):
    # folder_path = 'D://img/'
    folder_path = './img/'
    img_name = folder_path + str(index + 0) + '.jpg'
    with open(img_name,'wb') as file:
        html = requests.get(src)
        file.write(html.content)
        file.flush()
    file.close()
#执行方法
def main():
    url = 'https://movie.douban.com/'
    html = get_one_page(url)
    for index, item in enumerate(parse_one_page(html)):
        print(item)
        #write_img(index,item['img'])
        write_to_file(index,item)
        time.sleep(1)


#  聊天对话
dui_hua_list = ['你好','你也好。有什么吩咐？','今天天气不错','还好，风力才6级。','你这样把天聊死了','都是你教的好，呵呵','排版很个性','我会努力的']
command_list = ['打开百度','打开新浪','退出','最近的热映电影','写个网页','打开来看看']
robot_name = '[- - 小明真淘气 - -]：'


# 比较两个字符串，输出两个字符串的相似度
def compare_str(s1, s2):
    same_s = [i for i in s1 if i in s2]
    return 100 * same_s.__len__() / (len(s1)+len(s2))


# 比较字符串str1在 列表list1中的最大相似度的元素对应的值、索引
def get_max_rate_index(str1, list1):
    rate_list = [compare_str(str1, i) for i in list1]
    max_value = 0
    max_index = 0
    for i in range(rate_list.__len__()):
        if rate_list[i]>max_value:
            max_value = rate_list[i]
            max_index = i
    return max_value,max_index


# 命令执行的函数,根据str1的描述，执行对应命令
def command_run(str1):
    if '打开百度'.__eq__(str1):
        webbrowser.open('www.baidu.com')
        print(robot_name, '已为您打开了百度网站')
    elif '打开新浪'.__eq__(str1):
        webbrowser.open('www.sina.com.cn')
        print(robot_name, '已为您打开了新浪')
    elif '最近的热映电影'.__eq__(str1):
        url = 'https://movie.douban.com/'
        # print(url)
        html = get_one_page(url)
        # print(html)
        for index, item in enumerate(parse_one_page(html)):
            # print(index)
            write_img(index,item['img'])
            time.sleep(1)
        print(robot_name, '已为您下载了豆瓣中的热映电影的海报，保存到img文件夹中了')
    elif '写个网页'.__eq__(str1):
        url = 'https://movie.douban.com/'
        html = get_one_page(url)
        for index, item in enumerate(parse_one_page(html)):
            write_to_file(index, item)
            time.sleep(1)
        print(robot_name, '已为您使用电影海报写成html网页。需要现在打开吗？')
    elif '打开来看看'.__eq__(str1):
        webbrowser.open('yemian.html')
        print(robot_name, '已为您打开了该网页')
    else:
        # webbrowser.open('file://E:/教学安排/2018上半年/聊城大学一周支持/聊城大学/yemian.html')
        # webbrowser.open('yemian.html')
        print(robot_name,'您应该说“退出”')
        pass


# 对话入口
def main_talk():

    s = socket.socket()
    # 为服务器绑定地址
    s.bind(('127.0.0.1', 18080))
    # 开启监听
    s.listen(1)
    cs, c_addr = s.accept()  # 默认阻塞性的等待链接
    print('地址为{}的客户端连接成功'.format(c_addr))

    print(robot_name,'客官，您里面请。')
    flag = True
    while flag:
        #str_input = input('[ Input here please]： ').__str__()
        print('接收该客户端的数据')
        data = cs.recv(1024)  # 默认阻塞性的等待接收数据
        data = data.decode()
        if len(data) < 1:
            break
        print('接收到的数据为：{}'.format(data))


        str_input = data.__str__()
        if '退出'==str_input:
            print(robot_name,'小的告退')
            break
            # flag=False
        talk_rate,talk_index = get_max_rate_index(str_input, dui_hua_list)
        cmd_rate,cmd_index = get_max_rate_index(str_input, command_list)
        if talk_rate>cmd_rate: # 如果判断为对话，那么，在控制台输出下一句对话
            print(robot_name,dui_hua_list[talk_index+1])
            #data_out = data + ' server'
            data_out = dui_hua_list[talk_index+1]
            # 将这个数据发送给客户端
            print('给该客户端的响应数据为：{}'.format(data_out))
            cs.send(data_out.encode())
        else:  # 如果判断为命令，那么，执行命令函数
            print(robot_name,'马上执行您的命令')
            data_out = '马上执行您的命令'
            # 将这个数据发送给客户端
            print('给该客户端的响应数据为：{}'.format(data_out))
            cs.send(data_out.encode())
            command_run(command_list[cmd_index])

if __name__ == '__main__':
    # main()
    main_talk()
