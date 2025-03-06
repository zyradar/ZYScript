import os
import cv2
import numpy as np
import math
import shutil
import tkinter as tk
from tkinter import messagebox
import requests
from GetParameters import get_windowstate


class CheckDaset:
    def __init__(self):
        self.get_img_format = (".jpg", ".JPG", ".png")
        self.format = None
        self.save_img_format = None
        self.save_size = (1920, 1200)
        # （1920， 1200）图片基准下（线条粗细基准，字体大小基准, 点大小基准，字体y轴补偿）
        self.line_scale, self.text_scale, self.circle_scale, self.yawcompen_scale = 3, 1.5, 5, 1.1
        self.check_label = ['2', '3', '4', '5', '6', '7']
        self.open_window = False
        self.show_time = 0

    # 批量检查标签文件,路径要求为待检查标签的文件夹路径
    def check_txt(self, path):
        self.open_window, self.show_time = get_windowstate()
        count = 0
        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                file_path = os.path.join(path, filename)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                error = True
                for line in lines:
                    if len(lines) <= 0:
                        continue
                    line = line.strip()
                    if line:
                        items = line.split(' ')
                        if len(items) > 1:
                            if items[0] in self.check_label:
                                error = False
                    else:
                        continue
                if error:
                    self.write_error(path, file_path, filename, "cant't find or classes error in")
                try:
                    if self.open_window:
                        image_bytes = np.asarray(
                            bytearray(requests.get("https://pic.quanjing.com/28/h3/QJ5100545083.jpg@%21350h").content),
                            dtype=np.uint8)
                        img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
                        img = cv2.resize(img, (1920, 1200))
                        img = self.add_progress(img, count, len(os.listdir(path)), 1)
                        count += 1
                        self.take_gui(img)
                except:
                    messagebox.showinfo('警告', "本地计算机已启用代理，将禁用进度可视化")
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "check_txt任务已完成")

    # 批量检查图片尺寸并将不符合尺寸的图片变为规定尺寸，路径要求待检查图片的文件夹路径
    def check_imgsize(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        self.set_check_img()
        count = 1
        for filename in os.listdir(path):
            if filename.endswith(self.get_img_format):
                file_path = os.path.join(path, filename)
                with open(file_path, 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(file_path)
                if img.shape[0] != self.save_size[1] or img.shape[1] != self.save_size[0]:
                    self.write_error(path, file_path, filename, "The image size does not comply with the rules in")
                    img = cv2.resize(img, self.save_size)
                    if self.save_img_format:
                        success, encoded_image = cv2.imencode('.bmp', img)
                        if success:
                            with open(file_path.split('.')[0] + self.save_img_format, 'wb') as f:
                                f.write(encoded_image)
                        # cv2.imwrite(file_path.split('.')[0] + self.save_img_format, img)
                    else:
                        success, encoded_image = cv2.imencode('.bmp', img)
                        if success:
                            with open(file_path, 'wb') as f:
                                f.write(encoded_image)
                        # cv2.imwrite(file_path, img)
                    if self.open_window:
                        img = self.add_progress(img, count, len(os.listdir(path)), None)
                        count += 1
                        self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "check_imgsize任务已完成")

    # 5点神符校对
    def check_buffdata(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        count = 1
        for name in os.listdir(path):
            if name.endswith('.txt'):
                i = 0
                txt = os.path.join(path, name)
                with open(txt.replace('.txt', self.get_img_format), 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(txt.replace('.txt', self.get_img_format))
                img = cv2.resize(img, (1920, 1200))
                with open(txt, 'r') as f:
                    for line in f.readlines():
                        item = line.split(' ')
                        if len(item) > 11:
                            i = 5
                            x, y, w, h = item[1:5]
                            cv2.rectangle(img, (int((float(x) - float(w) / 2) * 640), int((float(y) - float(h) / 2) * 384)),
                                          (int((float(x) + float(w) / 2) * 640), int((float(y) + float(h) / 2) * 384)),
                                          color=(0, 0, 255), thickness=max(math.ceil((self.line_scale - 1) * img.shape[1] / 1920), 1), lineType=cv2.LINE_AA)
                        points = np.array(np.array(item[i+1:], dtype=float).reshape(int(len(item[i+1:])/2), 2) * np.array([img.shape[1], img.shape[0]]), dtype=int)
                        self.draw_label(img, points, None, count, len(os.listdir(path)))
                count += 1
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "check_buffdata任务已完成")

    # 4点装甲板校对
    def check_armordata(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        count = 1
        for name in os.listdir(path):
            if name.endswith('.txt'):
                txt = os.path.join(path, name)
                with open(txt.replace('.txt', self.get_img_format), 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(txt.replace('.txt', self.get_img_format))
                img = cv2.resize(img, (1920, 1200))
                with open(txt, 'r') as f:
                    for line in f.readlines():
                        item = line.split(' ')
                        points = np.array(np.array(item[1:], dtype=float).reshape(4, 2) * np.array([img.shape[1], img.shape[0]]), dtype=int)
                        self.draw_label(img, points, None, count, len(os.listdir(path)))
                count += 1
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "check_armordata任务已完成")

    # 兑换框校对
    def check_rockdata(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        count = 1
        for name in os.listdir(path):
            if name.endswith('.txt'):
                txt = os.path.join(path, name)
                with open(txt.replace('.txt', self.get_img_format), 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(txt.replace('.txt', self.get_img_format))
                img = cv2.resize(img, (1920, 1200))
                with open(txt, 'r') as f:
                    for line in f.readlines():
                        item = line.split(' ')
                        x = float(item[1])
                        y = float(item[2])
                        w = float(item[3])
                        h = float(item[4])
                        points = [str(x-w/2), str(y-h/2), str(x+w/2), str(y-h/2), str(x+w/2), str(y+h/2), str(x-w/2), str(y+h/2)]
                        item_type = [x for x in item[5:] if float(x) <= 0 or float(x) >= 1]
                        item_type.insert(0, item[0])
                        item = [x for x in item[5:] if 0 < float(x) < 1]
                        for i in range(len(points)):
                            item.insert(0, points[len(points) - 1 - i])
                        points = np.array(np.array(item, dtype=float).reshape(int(len(item)/2), 2) * np.array([img.shape[1], img.shape[0]]), dtype=int)
                        self.draw_label(img, points[:4], item_type[0], count, len(os.listdir(path)))
                        self.draw_label(img, points[4:], item_type[1:], count, len(os.listdir(path)))
                count += 1
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "check_rockdata任务已完成")

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

    # 写入错误
    def write_error(self, path, file_path, filename, warning):
        with open(path + "error.txt", 'a') as f:
            name = file_path.split('.')
            if filename.endswith('.txt'):
                try:
                    shutil.move(name[0] + ".txt", path + "error/" + filename.split('.')[0] + ".txt")
                except:
                    f.writelines(warning + name[0] + ".txt" + "\n")
            else:
                try:
                    shutil.move(name[0] + ".jpg", path + "error/" + filename.split('.')[0] + ".jpg")
                except:
                    f.writelines(warning + name[0] + ".jpg" + "\n")

    # 绘制标签
    def draw_label(self, img, points, point_type, count, counts):
        if len(points) <= 4:
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        cv2.polylines(img, [points], True, (255, 255, 255),
                      max(math.ceil(self.line_scale * img.shape[1] / 1920), 1), cv2.LINE_AA)  # 以折线画图
        for i in range(len(points)):
            if point_type:
                if len(point_type) == 1:
                    cv2.putText(img, "(" + point_type[0] + ")", (points[i][0], points[i][1]-40),
                                cv2.FONT_HERSHEY_DUPLEX, self.text_scale * img.shape[1] / 1920-0.8,
                                color, max(math.ceil(self.line_scale - 1 * img.shape[1] / 1920), 1), cv2.LINE_AA)
                    point_type = None
                else:
                    cv2.putText(img, "(" + point_type[i] + ")", (points[i][0], points[i][1]-40),
                                cv2.FONT_HERSHEY_DUPLEX, self.text_scale * img.shape[1] / 1920-0.8,
                                color, max(math.ceil(self.line_scale - 1 * img.shape[1] / 1920), 1), cv2.LINE_AA)
            cv2.putText(img, str(i), (points[i][0], points[i][1]),
                        cv2.FONT_HERSHEY_DUPLEX, self.text_scale * img.shape[1] / 1920,
                        color, max(math.ceil(self.line_scale - 1 * img.shape[1] / 1920), 1), cv2.LINE_AA)
            cv2.circle(img, (points[i][0], points[i][1]), max(math.ceil((self.circle_scale - 1) * img.shape[1] / 1920), 1),
                       color, thickness=-1)
        if self.open_window:
            img = self.add_progress(img, count, counts, None)
            self.take_gui(img)

    def set_check_img(self):
        set_window = tk.Tk()
        set_window.geometry("750x250")
        set_window.title("保存视频设置")
        tk.Label(set_window, text="处理后图片的格式，如‘.jpg’留空则默认原格式:", font=("Arial", 16)).grid(row=1, column=0, pady=10)
        imgformat_entry = tk.Entry(set_window, width=30)
        imgformat_entry.grid(row=1, column=1, pady=5)
        tk.Label(set_window, text="设置检查图片的大小尺寸，如‘1920,1200’(默认值):", font=("Arial", 16)).grid(row=2, column=0, pady=5)
        imgsize_entry = tk.Entry(set_window, width=30)
        imgsize_entry.grid(row=2, column=1, pady=5)

        def on_submit():                                    # 创建提交按钮
            self.save_img_format = imgformat_entry.get() if imgformat_entry.get() else self.save_img_format
            self.save_size = imgsize_entry.get() if imgsize_entry.get() else self.save_size
            set_window.destroy()                          # 关闭输入窗口
        tk.Button(set_window, text="提交", command=on_submit, width=20, bg="lightblue", font=("Arial", 16)).grid(row=6, column=0, columnspan=2, pady=40)
        set_window.wait_window()                          # 等待直到输入窗口关闭

    def get_format(self):
        getformat = tk.Tk()
        getformat.geometry("400x300")
        getformat.title("选择处理格式")
        tk.Label(getformat, text="请输入你要处理的文件格式\n如’.jpg‘，’.mp4‘\n关闭该窗口或输入空信息将使用默认格式:", font=("Arial", 14)).pack(pady=10)
        format_entry = tk.Entry(getformat, width=30, font=("Arial", 12))
        format_entry.pack(pady=10)

        def on_submit():                                    # 创建提交按钮
            self.format = format_entry.get() if format_entry.get() else ".jpg,.JPG,.png"
            self.format = list(i.strip(' ') for i in self.format.split(','))
            for i in self.format:
                if len(i.split('=')) > 1:
                    self.save_img_format = i.split('=')[1]
                    self.format[len(self.format)-1] = i.split('=')[0]
            self.format = tuple(self.format)
            getformat.destroy()                          # 关闭输入窗口
        tk.Button(getformat, text="提交", command=on_submit, width=20, bg="lightblue").pack(pady=10)
        getformat.wait_window()                          # 等待直到输入窗口关闭

    # 可视化界面
    def take_gui(self, img):
        cv2.namedWindow("gui", cv2.WINDOW_NORMAL)
        cv2.imshow("gui", img)
        if cv2.waitKey(self.show_time) == 27:
            self.open_window = False
            cv2.destroyAllWindows()


# CheckDaset().check_imgsize('C:/Users/HZY/Pictures/work/txt/')
# CheckDaset().check_imgsize('C:/Users/HZY/Pictures/work/txt/test/')

