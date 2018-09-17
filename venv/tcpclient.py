# 创建一个客户端，然后与tcp server进行通信
# 发送一个hello world 到服务器， 希望得到的响应是 welcome
import socket

# 创建套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接到server
print('开始请求服务器的连接。。。')
s.connect(('127.0.0.1', 18080))

# 连接上之后进行多次对话
while True:
    # 发送的数据可以手动输入
    input_s = input('请输入需要执行的命令或对话>>>')

    # 发送数据
    print('发送{} 到服务器'.format(input_s))
    s.send(input_s.encode())
    # 做个判断，如果输入的数据为空,那么停止通信，退出循环
    if len(input_s) < 1:
        break
    # 接收数据,并解码成字符串
    print('接收服务器的响应。。。')
    data = s.recv(1024).decode()
    # 。。。
    print('客户端接收到的数据为：', data)

# 关闭套接字
s.close()
