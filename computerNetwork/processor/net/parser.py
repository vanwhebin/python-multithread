# _*_ encoding=utf-8 _*_

import struct
import socket


class IPParser:
    IP_HEADER_LENGTH = 20

    @classmethod
    def parse_ip_header(cls, ip_header):
        """
        IP 报文格式
        line 1: 4位IP_version 4位ip头长度  16位服务类型
        line 2: 16位标识符  3位标记位  3位片位移
        line 3: 8位ttl   8位协议  16位IP头校验和
        line 4: 32位源IP地址
        line 5: 32位目的IP地址
        :param ip_header:
        :return:
        """
        line1 = struct.unpack(">BBH", ip_header[:4])
        # 11110000 => 1111
        ip_version = line1[0] >> 4
        # 11111111 => 00001111 & 00001111
        iph_length = line1[0] & 15 * 4
        pkg_length = line1[2]
        line3 = struct.unpack(">BBH", ip_header[8:12])
        ttl = line3[0]
        protocal = line3[1]
        iph_checksum = line3[2]
        line4 = struct.unpack(">4s", ip_header[12:16])  # 转化位4个arscII码
        src_ip = socket.inet_ntoa(line4[0])
        line5 = struct.unpack(">4s", ip_header[16:20])     # 转化位4个arscII码
        dst_ip = socket.inet_ntoa(line5[0])

        return {
            "ip_version": ip_version,
            "iph_length": iph_length,
            "packet_length": pkg_length,
            "ttl": ttl,
            "protocol": protocal,
            "iph_checksum": iph_checksum,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
        }

    @classmethod
    def parse(cls, ip_header):
        return cls.parse_ip_header(ip_header)

