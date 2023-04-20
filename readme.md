# Politics Analyze

## Data Sources

- nytimes
- guardian
- mediastack

## Local Steps

```bash
# 创建虚拟环境
python3 -m venv crawler

# 激活虚拟环境
source crawler/Scripts/activate

# 安装依赖
pip install -r requirements.txt

# 创建数据库并获取数据
python fetch_data.py

# 分析数据
python analyze.py

# 启动服务
python app.py

# 打开浏览器
http://localhost:8000
```

## Local Docker Steps

```bash
# 构建镜像并运行
docker-compose up -d --build

# 打开浏览器
http://localhost
```
