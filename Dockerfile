# 构建阶段(拉环境)
# 拉取一个轻量级的3.11版本的python作为基础镜像
FROM python:3.11-slim AS builder
# 新建一个工作文件夹，将基础镜像存放，在此进行工作
WORKDIR /app
# 将根目录的环境列表复制到当前文件夹
COPY requirements.txt .
# 读取环境列表，逐个下载
RUN pip install --no-cache-dir -r requirements.txt

#构建+运行(最终镜像)
#基础镜像
FROM python:3.11-slim
#工作文件夹
WORKDIR /app
#复制已经下载好的环境
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/pytest /usr/local/bin/pytest
#拉取代码
COPY . .
#运行(run)容器时，进行的操作(自动开始跑测试)
CMD ["pytest","-v","-s"]