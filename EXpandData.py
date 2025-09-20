import cv2
import numpy as np
import os
import math
import tkinter as tk
from tkinter import messagebox, simpledialog
from GetParameters import get_windowstate

class EXpandData:
    def __init__(self):
        self.col = 0
        self.heri = 0
        self.alpha = 100          # 对比度调整参数
        self.beta = 0           # 亮度调整参数
        self.exposure = 1       # 曝光倍数
        self.imgsize = (640, 384)
        self.get_img_format = ('.jpg', '.JPG', 'png')
        self.format = None
        self.perfix = "color_"
        self.color = "B"
        # （1920， 1200）图片基准下（线条粗细基准，字体大小基准，字体y轴补偿）
        self.line_scale, self.text_scale, self.yawcompen_scale = 3, 1.5, 1.1
        self.open_window = False
        self.show_time = 1

    def change_bright(self, path):
        with open(path, 'rb') as f:
            img_array = np.frombuffer(f.read(), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
        # img = cv2.imread(path)
        img = cv2.resize(img, (640, 384))
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        self.addtrackbar()
        while True:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)                                          # 转换为HSV色彩空间
            hsv[:, :, self.col] -= self.heri                                                    # 调整亮度，将亮度的值增加50
            img_hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)                                      # 转换回BGR色彩空间
            img_Scal = cv2.convertScaleAbs(img_hsv, alpha=self.alpha/100, beta=self.beta)       # 调整对比度，增加50%
            dst = np.power(img_Scal / 255., 1 / (self.exposure / 100 + 1))                      # 曝光
            dst = np.uint8(dst * 255)
            cv2.imshow('image', dst)
            name = os.listdir(path)
            if cv2.waitKey(1) == 27:
                break
        success, encoded_image = cv2.imencode('.bmp', dst)
        if success:
            with open(path + "exhigh_" + name, 'wb') as f:
                f.write(encoded_image)

    def brightData(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_multiple_inputs()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        count = 0
        counts = len(os.listdir(path))
        for name in os.listdir(path):
            if name.endswith(self.get_img_format):
                with open(path + name, 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(path + name)
                img = cv2.resize(img, self.imgsize)
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 转换为HSV色彩空间
                hsv[:, :, self.col] -= self.heri  # 调整亮度，将亮度的值增加50
                img_hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)  # 转换回BGR色彩空间
                img_Scal = cv2.convertScaleAbs(img_hsv, alpha=self.alpha / 100, beta=self.beta)  # 调整对比度，增加50%
                dst = np.power(img_Scal / 255., 1 / (self.exposure / 100 + 1))  # 曝光
                dst = np.uint8(dst * 255)
                success, encoded_image = cv2.imencode('.bmp', dst)
                if success:
                    with open(path + "exhigh_" + name, 'wb') as f:
                        f.write(encoded_image)
                # cv2.imwrite(path + "exhigh_" + name, dst)
                if self.open_window:
                    dst = self.add_progress(dst, count, counts, None)
                    count += 1
                    self.take_gui(dst)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "brightData任务已完成")

    def AntiColor(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        RED_TO_BLUE = [-0.1, 3.0, 0.0]
        BLUE_TO_RED = [-0.4, 0.2, 0.5]
        BLUE_TO_ORANGE = [-0.4, -.2, 0.5]
        count = 0
        counts = len(os.listdir(path))
        if self.color == "B":
            values = [BLUE_TO_RED, BLUE_TO_ORANGE]
        elif self.color == "R":
            values = [RED_TO_BLUE]
        for name in os.listdir(path):
            if name.endswith(self.get_img_format):
                with open(path + name, 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(path + name)
                hgain, sgain, vgain = values[0]
                r = np.array([hgain, sgain, vgain]) + 1  # random gains
                hue, sat, val = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
                dtype = img.dtype  # uint8
                x = np.arange(0, 256, dtype=np.int16)
                lut_hue = ((x * r[0]) % 180).astype(dtype)
                lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
                lut_val = np.clip(x * r[2], 0, 255).astype(dtype)
                img_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val))).astype(
                    dtype)
                cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR, dst=img)  # no return needed
                success, encoded_image = cv2.imencode('.bmp', img)
                if success:
                    with open(path + self.perfix + name, 'wb') as f:
                        f.write(encoded_image)
                # cv2.imwrite(path + self.perfix + name, img)
                if self.open_window:
                    img = self.add_progress(img, count, counts, None)
                    count += 1
                    self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "AntiColor任务已完成")

    def Arguments(self, x):
        self.alpha = cv2.getTrackbarPos('Alpha', 'image')
        self.beta = cv2.getTrackbarPos('Beta', 'image')
        self.heri = cv2.getTrackbarPos('heri', 'image')
        self.col = cv2.getTrackbarPos('col', 'image')
        self.exposure = cv2.getTrackbarPos('exposure', 'image')
        # messagebox.showinfo("参数确认", f"hsv通道值: {self.col}\n亮度（hsv三通道值）: {self.heri}\n"
        #                             f"RGB对比度系数: {self.alpha}\nRGB亮度值: {self.beta}\n曝光系数: {self.exposure}")

    def addtrackbar(self):
        cv2.createTrackbar('Alpha', 'image', 0, 500, self.Arguments)
        cv2.createTrackbar('Beta', 'image', 0, 255, self.Arguments)
        cv2.createTrackbar('heri', 'image', 0, 255, self.Arguments)
        cv2.createTrackbar('col', 'image', 0, 2, self.Arguments)
        cv2.createTrackbar('exposure', 'image', 0, 399, self.Arguments)

    def get_multiple_inputs(self):
        input_window = tk.Tk()
        input_window.title("请输入你要设置的参数")

        tk.Label(input_window, text="col(hsv，V层通道值):").grid(row=0, column=0, pady=5)
        col_entry = tk.Entry(input_window)
        col_entry.grid(row=0, column=1, pady=5)

        tk.Label(input_window, text="heri(亮度（hsv,V层三通道值）):").grid(row=1, column=0, pady=5)
        heri_entry = tk.Entry(input_window)
        heri_entry.grid(row=1, column=1, pady=5)

        tk.Label(input_window, text="alpha(RGB对比度系数):").grid(row=2, column=0, pady=5)
        alpha_entry = tk.Entry(input_window)
        alpha_entry.grid(row=2, column=1, pady=5)

        tk.Label(input_window, text="beta(RGB亮度值):").grid(row=3, column=0, pady=5)
        beta_entry = tk.Entry(input_window)
        beta_entry.grid(row=3, column=1, pady=5)

        tk.Label(input_window, text="exposure(曝光系数):").grid(row=4, column=0, pady=5)
        exposure_entry = tk.Entry(input_window)
        exposure_entry.grid(row=4, column=1, pady=5)

        def on_submit():                                    # 创建提交按钮
            self.col = int(col_entry.get())
            self.heri = int(heri_entry.get())
            self.alpha = int(alpha_entry.get())
            self.beta = int(exposure_entry.get())
            self.exposure = int(beta_entry.get())
            input_window.destroy()                          # 关闭输入窗口
            messagebox.showinfo("参数确认", f"col(hsv，V层通道值): {self.col}\nheri(亮度（hsv，V层三通道值）): {self.heri}\n"
                    f"alpha(RGB对比度系数): {self.alpha}\nbeta(RGB亮度值): {self.beta}\nexposure(曝光系数): {self.exposure}")
        submit_button = tk.Button(input_window, text="提交", command=on_submit)
        submit_button.grid(row=5, columnspan=2, pady=5)
        input_window.wait_window()                          # 等待直到输入窗口关闭

    def get_format(self):
        getformat = tk.Tk()
        getformat.geometry("400x300")
        getformat.title("选择处理格式")
        tk.Label(getformat, text="请输入你要处理的文件格式\n如’.jpg,.mp4‘，可处理多个或单个格式\n关闭该窗口或输入空信息将使用默认格式\n"
                                 "默认格式为('.jpg', '.JPG', 'png')", font=("Arial", 14)).pack(pady=10)
        format_entry = tk.Entry(getformat, width=30, font=("Arial", 12))
        format_entry.pack(pady=10)

        def on_submit():                                    # 创建提交按钮
            self.format = format_entry.get()
            try:
                self.format = tuple(i.strip(' ') for i in self.format.split(','))
            except:
                self.format = self.format
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

# EXpandData().change_bright('C:/Users/HZY/Pictures/work/txt/bule.jpg')
# EXpandData().brightData('C:/Users/HZY/Pictures/work/txt/')