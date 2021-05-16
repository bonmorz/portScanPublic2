# -*- coding: utf-8 -*-
import socket

import re
from scapy.all import *
import subprocess
import re
import xlrd

final_result={}


def read_usage():
    wb = xlrd.open_workbook('tcpUsage.xlsx')
    # 按工作簿定位工作表
    sh = wb.sheet_by_name('Sheet1')
    # print(sh.nrows)  # 有效数据行数
    # print(sh.ncols)  # 有效数据列数
    # print(sh.cell(0, 0).value)  # 输出第一行第一列的值
    # print(sh.row_values(0))  # 输出第一行的所有值
    # 将数据和标题组合成字典
    # print(dict(zip(sh.row_values(0), sh.row_values(1))))
    # 遍历excel，打印所有数据
    usage_result = []
    usage_dict = {}
    for i in range(sh.nrows):
        # print(sh.row_values(i))
        usage_dict[sh.row_values(i)[0]] = sh.row_values(i)[1]
    # print(usage_result)
    #print(usage_dict)
    return usage_dict

def get_port_status(server_ip, server_port,port_dict):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((server_ip, server_port))
        print('{} port {} is opened'.format(server_ip, server_port))
        print("用途是"+port_dict.get(int(server_port)))
        final_result[int(server_port)]=port_dict.get(int(server_port))

    except Exception as err:
        pass
    finally:
        s.close()

def get_target_system(ip):
    print("测试ip开始")

    p = subprocess.Popen(["ping", "-c", "5", ip], stdout=subprocess.PIPE)
    # print(p)
    res = p.communicate()[0]
    if p.returncode > 0:
        print('server error')
    else:
        pattern = re.compile('ttl=\d*')
        # print(pattern.search(str(res)).group())
        ttl = pattern.search(str(res)).group()
        ttl = int(ttl[4:])
        global system_check
        if ttl <= 64:
            print("Linux or Unix!")
            system_check = "Linux or Unix"
        elif ttl <= 128 and ttl > 64:
            print("Windows!")
            system_check="Windows"
        else:
            print("Unix!")
            system_check="Unix"

def main():
    usage_dict={}


    usage_dict=read_usage()
    ip = input('暂不支持域名\r\n请输入IP地址（默认为127.0.0.1）：')
    pattern_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    # pattern_cn = re.compile(r'(\w+\.){2}\w+')
    # host_cn = pattern_cn.match(ip)
    host_ip = pattern_ip.match(ip)
    if ip != '':
        if host_ip:
            #           socket.gethostbyname(ip)
            ip = host_ip.group()
        else:
            print('格式输入错误')
            exit(-1)
    else:
        ip = '127.0.0.1'

    get_target_system(ip)




    port = input('请输入端口,将扫描到该端口为止：')
    port = int(port)
    if port == '':
        port_start = 1
        port_end = 65536
        port = range(port_start, port_end)
        for p in port:
            get_port_status(ip, int(p),usage_dict)
    elif port != '':
        port_start = 1
        port_end = port
        port_list = range(port_start, port_end)
        for p in port_list:
            get_port_status(ip, int(p),usage_dict)

    else:
        get_port_status(ip, port)
    print(final_result)
    print(system_check)

if __name__ == '__main__':
    main()
