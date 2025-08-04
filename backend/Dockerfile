#/backend/Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 拷贝后端应用代码和配置
COPY backend/app /app/app
COPY backend/requirements.txt /app/requirements.txt
COPY frontend/templates /app/templates
COPY frontend/static /app/static

# 复制许可证及密钥
COPY license.lic public.pem /app/

# 安装依赖
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# 环境变量
ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=development

# 运行应用
CMD ["flask", "run", "--host=0.0.0.0"]
