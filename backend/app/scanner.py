#/ backend/app/scanner.py


import socket
import ipaddress
import threading
import os
import re
from queue import Queue
from scapy.all import sr1, IP, UDP, DNS, DNSQR

# 简单端口与服务指纹库
SERVICE_FINGERPRINTS = {
    22: 'SSH',
    80: 'HTTP',
    443: 'HTTPS',
    53: 'DNS',
    3306: 'MySQL',
    5432: 'PostgreSQL',
    6379: 'Redis',
    27017: 'MongoDB',
    21: 'FTP',
    23: 'Telnet',
    25: 'SMTP',
    110: 'POP3',
    143: 'IMAP'
}


def parse_target_ip(target):
    try:
        ip_net = ipaddress.ip_network(target, strict=False)
        return [str(ip) for ip in ip_net.hosts()]
    except ValueError:
        return [target]


def parse_ports(port_range):
    ports = set()
    for part in port_range.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)


def grab_banner(ip, port, timeout=1.0):
    try:
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.sendall(b'\r\n')
            return s.recv(1024).decode(errors='ignore').strip()
    except Exception:
        return None


def detect_service(port, banner):
    # 使用端口和banner的简单匹配
    if port in SERVICE_FINGERPRINTS:
        return SERVICE_FINGERPRINTS[port]
    if banner:
        if 'ssh' in banner.lower():
            return 'SSH'
        elif 'http' in banner.lower():
            return 'HTTP'
        elif 'smtp' in banner.lower():
            return 'SMTP'
    return 'Unknown'


def scan_tcp(ip, port, result_list, banner=False):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            banner_text = grab_banner(ip, port) if banner else None
            result_list.append({
                "ip": ip,
                "port": port,
                "status": "open",
                "protocol": "TCP",
                "banner": banner_text,
                "service": detect_service(port, banner_text)
            })
    except:
        pass


def scan_udp(ip, port, result_list):
    pkt = IP(dst=ip)/UDP(dport=port)/DNS(rd=1, qd=DNSQR(qname="example.com"))
    try:
        resp = sr1(pkt, timeout=1, verbose=0)
        if resp:
            result_list.append({
                "ip": ip,
                "port": port,
                "status": "open",
                "protocol": "UDP",
                "service": detect_service(port, None)
            })
    except:
        pass


def run_scan(target="127.0.0.1", ports="22,80", threads=100, banner=False, udp=False):
    target = resolve_target_ip(target)
    print(f"[DEBUG] Running scan: target={target}, ports={ports}, threads={threads}, banner={banner}, udp={udp}")
    result = []
    ip_list = parse_target_ip(target)
    port_list = parse_ports(ports)
    q = Queue()

    for ip in ip_list:
        for port in port_list:
            q.put((ip, port))

    def worker():
        while not q.empty():
            ip, port = q.get()
            if udp:
                scan_udp(ip, port, result)
            else:
                scan_tcp(ip, port, result, banner=banner)
            q.task_done()

    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.start()
        threads_list.append(t)

    q.join()
    for t in threads_list:
        t.join()

    return result


def resolve_target_ip(target):
    # Docker 内访问宿主机处理
    if target == "127.0.0.1":
        if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_ENV') == '1':
            return "172.17.0.1"

    # 如果是合法 IP，直接返回
    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        pass

    # 如果是主机名，尝试 DNS 解析
    try:
        resolved = socket.gethostbyname(target)
        return resolved
    except socket.gaierror:
        raise ValueError(f"❌ 无法解析目标：'{target}' 不是有效的 IP 或主机名")

