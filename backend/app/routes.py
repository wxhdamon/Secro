# /backend/app/routes.py

from flask import Blueprint, request, jsonify, render_template
from .license import check_license
from .scanner import run_scan
from .models import save_scan_result, load_scan_history
import ipaddress
import socket
import subprocess
import json

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/history')
def history():
    results = load_scan_history(limit=20)
    return render_template('history.html', results=results)

@main.route('/api/scan', methods=['POST'])
def scan():
    if not check_license():
        return jsonify({'error': 'Invalid or expired license'}), 403

    data = request.get_json()
    target = data.get('target', '127.0.0.1')
    if target in ['127.0.0.1', 'localhost']:
        target = 'host.docker.internal'

    ports = data.get('ports', '22,80,443')
    threads = int(data.get('threads', 100))
    banner = data.get('banner', False)
    udp = data.get('udp', False)

    try:
        # 安全提醒逻辑（支持主机名）
        resolved_ip = socket.gethostbyname(target.split('/')[0])
        ip = ipaddress.ip_address(resolved_ip)

        port_list = ports.split(',')
        if not ip.is_private and ('22' in port_list or any(p.startswith('22-') for p in port_list)):
            warning = "⚠️ Warning: You are scanning port 22 on a public IP. This may be considered intrusive."
        else:
            warning = None

        result = run_scan(target=target, ports=ports, threads=threads, banner=banner, udp=udp)
        save_scan_result(result)

        # 写入扫描结果供Perl使用
        with open('/tmp/scan_result.json', 'w') as f:
            json.dump(result, f)

        # 调用 Perl 分析脚本
        subprocess.run(['perl', 'app/analyze.pl', '/tmp/scan_result.json', '/tmp/analyzed.txt'], check=True)

        # 读取分析结果
        with open('/tmp/analyzed.txt', 'r') as f:
            analysis = f.read()

        return jsonify({
            'status': 'Scan completed',
            'result': result,
            'analysis': analysis,
            'warning': warning
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500