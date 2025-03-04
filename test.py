# GitHub 上的 script.py
import cv2
import numpy as np
import requests
print("🚀 这段代码是直接从 GitHub 加载并运行的！")

proxy = '127.0.0.1:7890'
proxies = {                                # netsh winhttp show proxy  查看代理服务器
    'http': 'http://' + proxy,            # HTTP 代理
    'https': 'http://' + proxy            # HTTPS 代理
}
# 可以定义函数
def hello():
    image_bytes = np.asarray(
        bytearray(requests.get("https://pic.quanjing.com/28/h3/QJ5100545083.jpg@%21350h", proxies=proxies).content),
        dtype=np.uint8)
    img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    cv2.namedWindow('jpg', cv2.WINDOW_NORMAL)
    cv2.imshow('jpg', img)
    cv2.waitKey(0)
    print("你好，GitHub 代码执行成功！")

# 甚至执行复杂操作
if __name__ == "__main__":
    hello()
