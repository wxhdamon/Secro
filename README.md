Secro：多语言集成的网络服务扫描与分析工具

项目简介
Secro 是一个结合Python、Perl和JavaScript的网络安全工具，用于扫描指定主机的开放端口、识别服务，并生成初步的服务分析报告。 
本项目旨在展示三种脚本语言的协同工作流程：
Python处理扫描任务，Perl负责文本分析，JavaScript实现前端界面与交互。

主流程：前端发送扫描请求 --> Flask校验授权 --> 调用扫描模块 --> 保存结果 --> 调用Perl脚本分析 --> 返回扫描和分析结果。

#快速开始
1.进入目录
pip install rsa(首次)

2.生成密钥（第一次）
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem

3.生成 license 文件
python3 scripts/license_generator.py

4.启动服务
docker-compose up --build

5.访问页面 localhost:8080

一、相关功能
网络端口扫描器（Python）
扫描结果分析统计
/*SSH 日志分析入侵检测（Perl）*/
扫描结果入库（PostgreSQL + SQLAlchemy）
Web 仪表盘（HTML + JS）
授权机制（.lic 文件 + RSA 签名验证）
Docker 一键部署

二、API说明
1. GET /
描述：访问主页，返回前端页面（index.html）。
用途：提供用户界面，包含按钮启动扫描、显示结果等。
响应：HTML 页面

2. POST /api/scan
描述：执行一次网络端口扫描任务。
授权校验：请求前会自动验证本地license.lic是否存在、合法、未过期。
请求参数：无（V1 默认扫描 127.0.0.1 的固定端口）
未来可扩展：支持POST提交自定义目标地址、端口范围等

逻辑流程：
检查 license
执行端口扫描（scanner.py）
将结果存入数据库（models.py > save_scan_result）
返回扫描结果 JSON
>响应格式（成功）：
{
  "status": "Scan completed",
  "result": [
    {"port": 22, "status": "open"},
    {"port": 80, "status": "closed"},
    ...
  ]
}
>响应格式（失败或无效 license）：
{ "error": "Invalid or expired license" }

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
│   │   ├── __init__.py             # 集中初始化Flask应用及其组件，如创建入口，注册，初始化DB等
│   │   ├── analyze.pl              # 对扫描数据做简单统计分析
│   │   ├── base.py                 # SQLAlchemy 基类定义（用于创建模型）
│   │   ├── config.py               # 数据库连接配置，支持环境变量
│   │   ├── db.py                   # 数据库引擎与会话管理器初始化
│   │   ├── license.py              # License 验证逻辑（基于 RSA 签名）
│   │   ├── models.py               # SQLAlchemy数据模型定义，如ScanResult表、save_scan_result(data)函数-保存扫描结果，load_scan_history(limit=20)加载扫描结果
│   │   ├── routes.py               # 路由与API定义（Flask蓝图），包括前端页面的访问路由（如/、/history），后端API接口接收前端请求，调用扫描逻辑、返回JSON或HTML页面
│   │   └── scanner.py              # 网络端口扫描逻辑（基于socket）
│   ├── Dockerfile                 # 构建后端镜像的 Dockerfile
│   └── requirements.txt           # 后端 Python 依赖列表
├── docker-compose.yml             # 整体容器编排文件（后端 + 数据库）
├── frontend                       # 前端资源目录
│   ├── static                     # 静态资源（JS / CSS）
│   │   ├── dashboard.js           # 控制扫描请求与结果显示的 JS 脚本
│   │   └── styles.css             # 样式表
│   └── templates
│       └── history.html           # 扫描历史记录页面
│       └── index.html             # 主界面 HTML 模板（Flask 使用 Jinja2 渲染）
├── LICENSE                        # 开源许可文件
├── license.lic                    # 授权 License 文件（包含签名和过期时间）
├── private.pem                    # RSA 私钥（用于生成 license.lic）
├── public.pem                     # RSA 公钥（后端用于验证 license）
├── README.md                      # 项目说明文档（功能、部署、使用方式等）
├── scripts                        # 辅助脚本目录
│   └── license_generator.py       # License 文件生成器（签名功能）