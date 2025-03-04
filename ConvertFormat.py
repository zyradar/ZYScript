import os
import json
import numpy as np
import math
import cv2
import tkinter as tk
from tkinter import messagebox
import requests
from GetParameters import get_windowstate


class Format:
    def __init__(self, ):
        self.imgSize = (1920, 1200)
        self.perfix = "ground_"
        self.get_img_format = '.jpg'
        self.format = None
        # （1920， 1200）图片基准下（线条粗细基准，字体大小基准，字体y轴补偿）
        self.line_scale, self.text_scale, self.yawcompen_scale = 3, 1.5, 1.1
        self.open_window = False
        self.show_time = 0

    # 标注神符所需的json格式转成txt格式
    def json_to_buff(self, path):
        self.open_window, self.show_time = get_windowstate()
        count = 0
        for name in [x for x in os.listdir(path) if ".json" in x]:
            with open(os.path.join(path, name), 'r') as file:
                output = []
                info = json.load(file)
                shapes = info.get("shapes")
                for x in shapes:
                    label = str(0)
                    points = x.get("points")
                    points = " ".join([str(i) for i in (sum((np.array(points, dtype=np.float64) / self.imgSize).tolist(), []))])
                    string = " ".join([label, points])       # 标签 + 5点
                    output.append(string)
            with open(os.path.join(path, name).replace('.json', '.txt'), 'w') as file:
                for line in output:
                    file.write(line + '\n')
            if self.open_window:
                image_bytes = np.asarray(
                    bytearray(requests.get("https://pic.quanjing.com/28/h3/QJ5100545083.jpg@%21350h").content),
                    dtype=np.uint8)
                img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (1920, 1200))
                img = self.add_progress(img, count, len(os.listdir(path)), 1)
                count += 1
                self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "json_to_buff任务已完成")

    # 将json格式转换成txt格式
    def json_to_txt(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        count = 0
        for name in os.listdir(path):
            if name.endswith(self.get_img_format):
                with open(path + name, 'r') as f:       # 打开 JSON 文件并加载数据
                    data = json.load(f)
                output_str = json.dumps(data)           # 将数据转换为字符串格式
                with open(path, 'w') as f:              # 写入 TXT 文件
                    f.write(output_str)
            if self.open_window:
                image_bytes = np.asarray(
                    bytearray(requests.get("https://pic.quanjing.com/28/h3/QJ5100545083.jpg@%21350h").content),
                    dtype=np.uint8)
                img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (1920, 1200))
                img = self.add_progress(img, count, len(os.listdir(path)), 1)
                count += 1
                self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "json_to_txt任务已完成")

    # 在正常的数据集标签框前添加xywh矩形框
    def label_add_xywh(self, path):
        self.open_window, self.show_time = get_windowstate()
        count = 0
        counts = len(os.listdir(path))/2
        os.makedirs(path + "test/", exist_ok=True)  # 创建文件夹
        for filename in os.listdir(path):
            if filename.endswith('.txt'):  # 只处理txt文件
                file_path = os.path.join(path, filename)
                name = filename.split('.')
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                allline = []
                for line in lines:
                    line = line.strip()
                    if line:
                        with open(path + name[0] + self.get_img_format, 'rb') as f:
                            img_array = np.frombuffer(f.read(), dtype=np.uint8)
                        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                        # img = cv2.imread(path + name[0] + self.get_img_format)
                        dst = img.copy()
                        success, encoded_image = cv2.imencode('.bmp', img)
                        if success:
                            with open(path + "test/" + self.perfix + name[0] + ".jpg", 'wb') as f:
                                f.write(encoded_image)
                        # cv2.imwrite(path + "test/" + self.perfix + name[0] + ".jpg", img)
                        items = line.split(' ')
                        if len(items) != 13 or len(items) != 15:
                            xywh = self.get_rectangle(items, 0)
                            for i in range(len(xywh)):
                                items.insert(1, str(xywh[3-i]))
                            allline.append(' '.join(items) + '\n')
                        with open(path + "test/" + self.perfix + filename.split('.')[0] + ".txt", 'w') as f:
                            f.writelines(allline)
                        if self.open_window:
                            self.getROI(dst, items, count, counts)
                count += 1
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "label_add_xywh任务已完成")

    # 去除数据集标签中的xywh矩形框
    def label_cut_xywh(self, path):
        self.open_window, self.show_time = get_windowstate()
        count = 0
        for filename in os.listdir(path):
            if filename.endswith('.txt'):  # 只处理txt文件
                file_path = os.path.join(path, filename)  # 拼接路径
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                allline = []
                for line in lines:
                    line = line.strip()
                    if line:
                        items = line.split(' ')
                        for a in range(0, 4):
                            items.remove(items[1])
                        allline.append(' '.join(items) + '\n')
                with open(path + filename.split('.')[0] + ".txt", 'w') as f:
                    f.writelines(allline)
                if self.open_window:
                    image_bytes = np.asarray(
                        bytearray(requests.get("https://pic.quanjing.com/28/h3/QJ5100545083.jpg@%21350h").content),
                        dtype=np.uint8)
                    img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                    img = cv2.resize(img, (1920, 1200))
                    img = self.add_progress(img, count, len(os.listdir(path)), 1)
                    count += 1
                    self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "label_cut_xywh任务已完成")

    def get_rectangle(self, xywh, goal_type):
        if goal_type:
            xywh = list(map(float, xywh))
            xmax = max(xywh[0]+xywh[2]/2, xywh[4]+xywh[6]/2)
            ymax = max(xywh[1]+xywh[3]/2, xywh[5]+xywh[7]/2)
            xmin = min(xywh[0]-xywh[2]/2, xywh[4]-xywh[6]/2)
            ymin = min(xywh[1]-xywh[3]/2, xywh[5]-xywh[7]/2)
        else:
            xmax = max(max(float(xywh[1]), float(xywh[3])), max(float(xywh[5]), float(xywh[7])))
            ymax = max(max(float(xywh[2]), float(xywh[4])), max(float(xywh[6]), float(xywh[8])))
            xmin = min(min(float(xywh[1]), float(xywh[3])), min(float(xywh[5]), float(xywh[7])))
            ymin = min(min(float(xywh[2]), float(xywh[4])), min(float(xywh[6]), float(xywh[8])))
            if len(xywh) == 11:
                xmax = max(xmax, float(xywh[9]))
                ymax = max(ymax, float(xywh[10]))
                xmin = min(xmin, float(xywh[9]))
                ymin = min(ymin, float(xywh[10]))
            xmin -= 10/640
            ymin -= 10/384
            xmax += 10/640
            ymax += 10/384
        centerx = (xmax + xmin) / 2
        centery = (ymax + ymin) / 2
        w = xmax - xmin
        h = ymax - ymin
        return [centerx, centery, w, h]

    def getROI(self, img, items, count, counts):
        points = [int((float(items[1]) - float(items[3]) / 2) * 640), int((float(items[2]) - float(items[4]) / 2) * 384),
                  int((float(items[1]) + float(items[3]) / 2) * 640), int((float(items[2]) - float(items[4]) / 2) * 384),
                  int((float(items[1]) + float(items[3]) / 2) * 640), int((float(items[2]) + float(items[4]) / 2) * 384),
                  int((float(items[1]) - float(items[3]) / 2) * 640), int((float(items[2]) + float(items[4]) / 2) * 384),]
        points = np.array(np.array(points, dtype=float).reshape(4, 2), dtype=int)
        cv2.polylines(img, [points], True, (255, 255, 255), 1, cv2.LINE_AA)  # 以折线画图
        img = self.add_progress(img, count, counts, None)
        self.take_gui(img)

    def get_format(self):
        getformat = tk.Tk()
        getformat.geometry("400x300")
        getformat.title("选择处理格式")
        tk.Label(getformat, text="请输入你要处理的文件格式\n如’.jpg‘或’.png‘,请勿输入多个格式\n关闭该窗口或输入空信息将使用默认格式\n"
                                 "默认格式：.jpg", font=("Arial", 14)).pack(pady=10)
        format_entry = tk.Entry(getformat, width=30, font=("Arial", 12))
        format_entry.pack(pady=10)

        def on_submit():                                    # 创建提交按钮
            self.format = format_entry.get()
            # self.format = tuple(i.strip(' ') for i in self.format.split(','))
            getformat.destroy()                          # 关闭输入窗口
        tk.Button(getformat, text="提交", command=on_submit, width=20, bg="lightblue").pack(pady=10)
        getformat.wait_window()                          # 等待直到输入窗口关闭

    # 添加工作进度条
    def add_progress(self, img, count, counts, value):
        if value:
            color = (0, 0, 255)
        else:
            color = (255, 255, 255)
        rectangle_points = np.array([[int(img.shape[1] / 10 * 4), int(img.shape[0] / 30)],
                                     [int(img.shape[1] / 10 * 6), int(img.shape[0] / 30)],
                                     [int(img.shape[1] / 10 * 6), int(img.shape[0] / 30 * 2)],
                                     [int(img.shape[1] / 10 * 4), int(img.shape[0] / 30 * 2)]], np.int32)
        cv2.polylines(img, [rectangle_points], True, (0, 0, 255),
                      max(math.ceil(self.line_scale * img.shape[1] / 1920), 1), cv2.LINE_AA)
        img[int(img.shape[0] / 30):int(img.shape[0] / 15), int(img.shape[1] * 0.4):
            int(img.shape[1] * 0.4) + math.ceil(count / (5 * counts / img.shape[1]))] = (0, 0, 255)
        cv2.putText(img, str(count) + '/' + str(counts),
                    (int(img.shape[1] / 10 * 6), int(img.shape[0] / (15*self.yawcompen_scale))),
                    cv2.FONT_HERSHEY_DUPLEX, self.text_scale * img.shape[1] / 1920, color,
                    max(math.ceil(self.line_scale * img.shape[1] / 1920), 1), cv2.LINE_AA)
        if count / counts > 0.61:
            cv2.putText(img, str(round(float(count / counts) * 100, 2)) + '%...',
                        (int(img.shape[1] * 0.4) + math.ceil(0.61 * img.shape[1] / 5),
                         int(img.shape[0] / (15 * self.yawcompen_scale))), cv2.FONT_HERSHEY_DUPLEX,
                        (self.text_scale - 0.5) * img.shape[1] / 1920, (0, 255, 0),
                        max(math.ceil((self.line_scale - 1) * img.shape[1] / 1920), 1), cv2.LINE_AA)
        else:
            cv2.putText(img, str(round(float(count / counts) * 100, 2)) + '%...',
                        (int(img.shape[1] * 0.4) + math.ceil(count / (5 * counts / img.shape[1])),
                         int(img.shape[0] / (15 * self.yawcompen_scale))), cv2.FONT_HERSHEY_DUPLEX,
                        (self.text_scale - 0.5) * img.shape[1] / 1920, (0, 0, 255),
                        max(math.ceil((self.line_scale - 1) * img.shape[1] / 1920), 1), cv2.LINE_AA)
        return img

    def take_gui(self, img):
        cv2.namedWindow("gui", cv2.WINDOW_NORMAL)
        cv2.imshow("gui", img)
        if cv2.waitKey(self.show_time) == 27:
            self.open_window = False
            cv2.destroyAllWindows()


# Format().label_cut_xywh('C:/Users/HZY/Pictures/work/txt/')

