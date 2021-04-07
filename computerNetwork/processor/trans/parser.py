
import struct


class TransParser:

    IP_HEADER_OFFSET = 20
    UDP_HEADER_LENGTH = 8
    TCP_HEADER_LENGTH = 20


def data2str(data):
    l = len(data)
    data - struct.unpack(l*"B", data)
    string = ""
    for ch in data:
        if ch >= 127 or ch < 32:
            string += '.'
        else:
            string += chr(ch)

    return string


class UDPParser(TransParser):
    """
    line 1: 16位源端口  16位目的端口
    line 2: 16位UDP长度  16位UDP校验和
    """

    @classmethod
    def parse_udp_header(cls, udp_header):
        udp_header = struct.unpack(">HHHH", udp_header)

        return {
            "src_port": udp_header[0],
            "dst_port": udp_header[1],
            "udp_length": udp_header[2],
            "udp_checksum": udp_header[3],
        }

    @classmethod
    def parse(cls, packet):
        header_offset = cls.IP_HEADER_OFFSET + cls.UDP_HEADER_LENGTH
        udp_header = packet[cls.IP_HEADER_OFFSET: header_offset]
        data = packet[header_offset:]
        result = cls.parse_udp_header(udp_header)
        result['data'] = data2str(data)
        return result


class TCPParser(TransParser):

    @classmethod
    def parse_tcp_header(cls, tcp_header):
        """
        TCP header 结构
        line 1： 16位源端口  16位目的端口
        line 1： 序列号
        line 1： 确认号
        line 1： 4位数据偏移  6位保留字段  6位标志位  窗口大小
        line 1： 校验和  紧急指针
        :param tcp_header:
        :return:
        """

        line1 = struct.unpack(">HH", tcp_header[:4])
        src_port = line1[0]
        dst_port = line1[1]

        line2 = struct.unpack(">L", tcp_header[4:8])
        seq_num = line2[0]

        line3 = struct.unpack(">L", tcp_header[8:12])
        ack_num = line3[0]

        line4 = struct.unpack(">BBH", tcp_header[12:16])
        data_offset = line4[0] >> 4
        flags = line4[1] & int('001111111', 2)
        FIN = flags & 1
        SYN = (flags >> 1) & 1
        RST = (flags >> 2) & 1
        PSH = (flags >> 3) & 1
        ACK = (flags >> 4) & 1
        URG = (flags >> 5) & 1

        win_size = line4[2]

        line5 = struct.unpack(">HH", tcp_header[16:20])
        checksum = line5[0]
        urg_index = line5[1]

        return {
            "src_port": src_port,
            "dst_port": dst_port,
            "seq_num": seq_num,
            "ack_num": ack_num,
            "data_offset": data_offset,
            "flag": {
                "FIN": FIN,
                "SYN": SYN,
                "RST": RST,
                "PSH": PSH,
                "ACK": ACK,
                "URG": URG
            },
            "win_size": win_size,
            "checksum": checksum,
            "urg_index": urg_index
        }

    @classmethod
    def parse(cls, packet):
        header_offset = cls.IP_HEADER_OFFSET + cls.TCP_HEADER_LENGTH
        tcp_header = packet[cls.IP_HEADER_OFFSET: header_offset]
        data = packet[header_offset:]
        result = cls.parse_tcp_header(tcp_header)
        result['data'] = data2str(data)
        return result
