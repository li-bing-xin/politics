## politics

### sources

- nytimes
- guardian
- mediastack

### setps

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建数据库
python init_db.py

# 搞数据
# 1. guardian
cd guardian
python fetch.py

# 2. mediastack
cd mediastack
python fetch.py

# 3. nytimes
cd nytimes
python fetch.py
python saveData.py
```
