# Secro Security Platform

Lightweight enterprise tool for network scanning and log analysis.

# 快速开始
1. 解压后进入目录
cd secro
pip install rsa(首次)

2. 生成密钥（第一次）
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

3. 生成 license 文件
python3 scripts/license_generator.py

4. 启动服务
docker-compose up --build

一、功能概览
网络端口扫描器（Python）
SSH 日志分析入侵检测（Perl）
扫描结果入库（PostgreSQL + SQLAlchemy）
Web 仪表盘（HTML + JS）
授权机制（.lic 文件 + RSA 签名验证）
Docker 一键部署

二、API说明
POST /api/scan
参数	无需
返回值	JSON 格式的扫描结果列表
鉴权	自动读取 license.lic 验证签名与过期日期
{
  "status": "Scan completed",
  "result": [
    {"port": 22, "status": "open"},
    {"port": 80, "status": "closed"}
  ]
}

.lic 文件结构如下：
{
  "customer": "Acme Corp",
  "mac": "00:1A:2B:3C:4D:5E",
  "expires": "2026-01-01",
  "features": ["scanner", "parser"],
  "signature": "base64..."
}
三、代码结构目录说明    
目录/文件	                     描述
backend/app/	                Flask、数据库和应用代码（scanner, license, log_parser.pl 等）
frontend/	                    JS仪表盘前端页面
scripts/license_generator.py	生成授权文件脚本
docker-compose.yml	            一键部署所有服务
log_parser.pl	                Perl 编写日志解析器