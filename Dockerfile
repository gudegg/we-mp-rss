FROM ac2-registry.cn-hangzhou.cr.aliyuncs.com/ac2/base:ubuntu24.04-py312

# 安装系统依赖
# RUN apt-get install -y firefox 


WORKDIR /app

# 复制Python依赖文件
COPY requirements.txt .

# 安装Python依赖
# RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY . .


# 暴露端口
EXPOSE 8001

# 启动命令
# CMD ["uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8001"]
# CMD ["python", "main.py"]
CMD ["python"]