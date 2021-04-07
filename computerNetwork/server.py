
import json
import socket
from multiThreading.pool import ThreadPool as TP
from multiThreading.task import AsyncTask
from computerNetwork.processor.net.parser import IPParser
from computerNetwork.processor.trans.parser import UDPParser, TCPParser


class ProcessTask(AsyncTask):

    def __init__(self, packet, *args, **kwargs):
        self.packet = packet
        super(AsyncTask, self).__init__(func=self.process, *args, **kwargs)

    def process(self):
        headers = {
            "network_header": None,
            "transport_header": None,
        }
        ip_header = IPParser.parse(self.packet)
        if ip_header['protocol'] == 17:
            # UDP头部解析
            ip_header['transport_header'] = UDPParser.parse(self.packet)
        elif ip_header['protocol'] == 6:
            # TCP头部解析
            ip_header['transport_header'] = TCPParser.parse(self.packet)
        return ip_header


class Server:

    def __init__(self):
        # 工作协议类型IPv4。 套接字类型， 工作具体的协议IP协议
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.ip = "192.168.0.103"
        self.port = 6666
        self.sock.bind((self.ip, self.port),)

        # 混杂模式

        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        self.pool = TP(10)
        TP.start()

    def loop_serve(self):
        while True:
            # 接收
            packet, address = self.sock.recvfrom(65535)
            # 生成task
            task = ProcessTask(packet)
            # 投入线程池处理
            self.pool.put(task)
            # 获取结果
            result = task.get_result()
            result = json.dumps(result, indent=4)
            print(result)


if __name__ == "__main__":
    server = Server()
    server.loop_serve()
