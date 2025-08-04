# Secro Security Platform

Lightweight enterprise tool for network scanning and log analysis.

# 快速开始
1. 解压后进入目录
pip install rsa(首次)

2. 生成密钥（第一次）
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

3. 生成 license 文件
python3 scripts/license_generator.py

4. 启动服务
docker-compose up --build

一、相关功能
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
Secro
├── backend                         # 后端服务目录（基于 Flask 实现）
│   ├── app                         # 后端核心代码
│   │   ├── __init__.py             # Flask 应用创建入口，注册，初始化 DB
│   │   ├── base.py                 # SQLAlchemy 基类定义（用于创建模型）
│   │   ├── config.py               # 数据库连接配置，支持环境变量
│   │   ├── db.py                   # 数据库引擎与会话管理器初始化
│   │   ├── license.py              # License 验证逻辑（基于 RSA 签名）
│   │   ├── log_parser.pl           # Perl 脚本：日志扫描器（检测 SSH 登录失败等）
│   │   ├── models.py               # SQLAlchemy 数据模型定义（如 ScanResult）
│   │   ├── routes.py               # 路由与 API 定义（如 /api/scan）
│   │   └── scanner.py              # 网络端口扫描逻辑（基于 socket）
│   ├── Dockerfile                 # 构建后端镜像的 Dockerfile
│   └── requirements.txt           # 后端 Python 依赖列表
├── docker-compose.yml             # 整体容器编排文件（后端 + 数据库）
├── frontend                       # 前端资源目录
│   ├── static                     # 静态资源（JS / CSS）
│   │   ├── dashboard.js           # 控制扫描请求与结果显示的 JS 脚本
│   │   └── styles.css             # 样式表
│   └── templates
│       └── index.html             # 主界面 HTML 模板（Flask 使用 Jinja2 渲染）
├── LICENSE                        # 开源许可文件
├── license.lic                    # 授权 License 文件（包含签名和过期时间）
├── private.pem                    # RSA 私钥（用于生成 license.lic）
├── public.pem                     # RSA 公钥（后端用于验证 license）
├── README.md                      # 项目说明文档（功能、部署、使用方式等）
├── scripts                        # 辅助脚本目录
│   └── license_generator.py       # License 文件生成器（签名功能）