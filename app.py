import os
from multiprocessing import Process

# 本地直接启动并预览的话，执行本文件

PORT = 8000

def start_server():
    # 启动后端
    os.system("python ./visual/server/server.py")

def start_web():
    # 用http.server启动前端
    os.system("python -m http.server " + str(PORT) +  " --directory ./visual/web/")

def start_browser():
    # 用浏览器打开localhost:8000
    os.system("start http://localhost:" + str(PORT))

if __name__ == '__main__':
    p1 = Process(target=start_server)
    p2 = Process(target=start_web)
    # p3 = Process(target=start_browser)

    p1.start()
    p2.start()
    # p3.start()
