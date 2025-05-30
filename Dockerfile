# 使用官方 Python 镜像作为基础
FROM m.daocloud.io/docker.io/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目下的所有文件复制到容器的工作目录中
COPY . .

# 复制依赖列表并安装
RUN pip install -r requirements.txt

# 暴露 Flask 默认端口（通常为 5000）
EXPOSE 5000

# 启动命令
CMD ["python", "src/app.py"]
