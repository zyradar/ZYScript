import os
import cv2
import numpy as np
import math
import tkinter as tk
from tkinter import messagebox
import requests
from GetParameters import get_windowstate


class DataSet:
    def __init__(self):
        self.roi_flag = False                               # 是否开启ROI标点
        self.get_img_format = ('.jpg', '.JPG', '.png', '.png', '.txt')
        self.get_video_format = ('.mp4', '.avi')
        self.format = None
        self.save_path = "C:/Users/HZY/Pictures/work/txt/"
        self.video_name = '10.avi'
        # # 视频编码，依次为MPEG-4编码.mp4,MPEG-4编码.mp4,YUV编码.avi,MPEG-1编码.avi,MPEG-4编码.avi,OggVorbis.ogv,Flash视频.flv
        self.video_format = {'MPEG-4.mp4': ('M', 'P', '4', 'V'), 'H.264.mp4': ('X', '2', '6', '4'),
                             'YUV-4.avi': ('I', '4', '2', '0'), 'MPEG-1.avi': ('P', 'I', 'M', 'I'),
                             'MPEG-4.avi': ('X', 'V', 'I', 'D'), 'OggVorbis.ogv': ('T', 'H', 'E', 'O'),
                             'Flash.flv': ('F', 'L', 'V', '1')}
        self.set_videoformat = 'MPEG-4.avi'
        self.save_video_fps = 150
        self.save_size = (1920, 1200)
        self.save_img_format = ".jpg"
        self.perfix = 'buff'                           # 为数据集设置前缀
        self.frame_interval = 1                            # 视频读取数据集时间隔多少帧取一张图片
        self.scale = [8, 1, 1]                              # 训练集，验证集，测试集比例因子
        self.count = 1                                      # 帧数计数变量量
        self.i = 0                                          # 数据集编号
        self.start_count = 0
        self.position = []
        self.D_value = [1, 1]
        # （1920， 1200）图片基准下（线条粗细基准，字体大小基准，字体y轴补偿）
        self.line_scale, self.text_scale, self.yawcompen_scale = 3, 1.5, 1.1
        self.open_window = False                             # 是否开启图片预览
        self.show_time = 1                                  # 设置每次imshow多少毫秒

    # 传入视频制作数据集，路径要求为一个存放各个视频的文件夹路径或者单个视频路径
    def video_to_daset(self, path):
        self.count = 0
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_video_format = self.format
        counts = 0
        if self.open_window:
            messagebox.showinfo('清注意！！', "如果出现报错，可能原因是你的视频编码不完整，无法读取帧数信息，关闭可视化界面仍然可以正常实现原功能")
            if os.path.isdir(path):
                for name in os.listdir(path):
                    if name.endswith(self.get_video_format):
                        counts += int(cv2.VideoCapture(path + name).get(cv2.CAP_PROP_FRAME_COUNT))
            else:
                counts += int(cv2.VideoCapture(path).get(cv2.CAP_PROP_FRAME_COUNT))
        if os.path.isdir(path):
            for name in os.listdir(path):
                if name.endswith(self.get_video_format):
                    self.write_daset(path + name, counts)
        else:
            self.write_daset(path, counts)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "video_to_daset任务已完成")

    # 将图片制作成视频，路径要求为一个存放图片文件的文件夹路径
    def image_to_video(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        self.set_save_video()
        count = 1
        getvideo = cv2.VideoWriter(path + self.video_name, cv2.VideoWriter_fourcc(*self.video_format[self.set_videoformat]),
                                   self.save_video_fps, self.save_size)
        for name in os.listdir(path):
            if name.endswith(self.get_img_format):
                with open(path + name, 'rb') as f:
                    img_array = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                # img = cv2.imread(path + name)
                img = cv2.resize(img, self.save_size)
                getvideo.write(img)
                if self.open_window:
                    img = self.add_progress(img, count, len(os.listdir(path)), None)
                    count += 1
                    self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "image_to_video任务已完成")

    # 规定拼接顺序为索引顺序，将视频集自动拼接成方形阵图，img拼接，需自行设置每个图像之间间隔差，路径要求为存放视频的文件夹
    def montage_video(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        self.set_save_video()
        cap, img = [], []
        count = 1
        counts = 0
        for name in os.listdir(path):
            cap.append(cv2.VideoCapture(path + name))
            counts = max(counts, int(cv2.VideoCapture(path + name).get(cv2.CAP_PROP_FRAME_COUNT)))
        getvideo = cv2.VideoWriter(path + self.video_name, cv2.VideoWriter_fourcc(*self.video_format[self.set_videoformat]),
                                   self.save_video_fps, self.save_size)
        row_number = math.ceil(math.sqrt(len(cap)))
        dst_size = [(1200 + self.D_value[1]) * int(len(cap)/row_number) - self.D_value[1],
                    (1920 + self.D_value[0]) * row_number - self.D_value[0]]
        dst = np.zeros((dst_size[0], dst_size[1], 3), dtype=np.uint8)
        while True:
            startpoint = [0, 0]
            shutdown = 0
            for i in range(len(cap)):
                try:
                    img.append(cv2.resize(cap[i].read()[1], (1920, 1200)))
                except:
                    shutdown += 1
                    img.append(np.zeros((1200, 1920, 3), dtype=np.uint8))
                dst[startpoint[0]:img[i].shape[0], startpoint[1]:startpoint[1] + img[i].shape[1]] = img[i]
                startpoint[1] += img[i].shape[1] + self.D_value[1]                                      # x轴上递加拼接
                if (i + 1) % row_number == 0:
                    startpoint[0] += 1200 + self.D_value[0]                                             # 第二行开始
                    startpoint[1] = 0                                                                   # x轴拼接位置重置
            if shutdown == len(cap):
                break
            getvideo.write(cv2.resize(dst, self.save_size))
            if self.open_window:
                if count == 1:
                    messagebox.showinfo('清注意！！', "如果出现报错，可能原因是你的视频编码不完整，无法读取帧数信息，关闭可视化界面仍然可以正常实现原功能")
                dst = self.add_progress(dst, count, counts, None)
                count += 1
                self.take_gui(dst)
            img.clear()
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "montage_video任务已完成")

    # 按读入路径顺序将各个视频首尾连接起来，路径要求为存放各个视频的文件夹路径
    def connect_video(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        self.set_save_video()
        cap = []
        count = 1
        counts = 0
        for name in os.listdir(path):
            cap.append(cv2.VideoCapture(path + name))
            counts += int(cv2.VideoCapture(path + name).get(cv2.CAP_PROP_FRAME_COUNT))
        getvideo = cv2.VideoWriter(path + self.video_name, cv2.VideoWriter_fourcc(*self.video_format[self.set_videoformat]),
                                   self.save_video_fps, self.save_size)
        for i in range(len(cap)):
            while True:
                ret, img = cap[i].read()
                if not ret:
                    break
                img = cv2.resize(img, self.save_size)
                getvideo.write(img)
                if self.open_window:
                    if count == 1:
                        messagebox.showinfo('清注意！！', "如果出现报错，可能原因是你的视频编码不完整，无法读取帧数信息，关闭可视化界面仍然可以正常实现原功能")
                    img = self.add_progress(img, count, counts, None)
                    count += 1
                    self.take_gui(img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "connect_video任务已完成")

    # 当数据集中各类定义的对象变化时，提供批量修改数据集中类的工具，路径要求为一个存放待修改txt文件的文件夹路径
    # 对于要如何对txt文件中的类别进行修改需要根据自己的需求在源码中更改，源码中已给定实例参考
    def modify_classes(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        # 遍历文件夹内所有文件
        for filename in os.listdir(path):
            if filename.endswith('.txt'):  # 只处理txt文件
                file_path = os.path.join(path, filename)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                new_lines = []
                for line in lines:
                    line = line.strip()
                    if line:
                        items = line.split(' ')
                        if len(items) > 1:
                            if items[0] != '13':        # 强行替换为某一类
                                items[0] = '13'
                            items_copy = items.copy()
                            if items[0] == '13':        # 复制一行并替换类别
                                items_copy[0] = '4'
                                items[0] = '8'
                            # elif items[0] == '14':
                            #     items_copy[0] = '5'
                            #     items[0] = '8'
                            new_lines.append(' '.join(items) + '\n')
                            new_lines.append(' '.join(items_copy) + '\n')
                        else:
                            # items[0] = '28'
                            new_lines.append(' '.join(items) + '\n')
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)

    # 批量重命名，路径要求为文件夹
    def rename_file(self, path):
        self.open_window, self.show_time = get_windowstate()
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        count = 0
        for old_name in os.listdir(path):
            if old_name.endswith(self.get_img_format):
                new_name = self.perfix + old_name  # 根据文件名格式生成新的文件名
                os.rename(os.path.join(path, old_name), os.path.join(path, new_name))  # 重命名文件
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
        messagebox.showinfo('温馨提示', "rename_file任务已完成")

    # 通过视频制作数据集
    def write_daset(self, avipath, counts):
        cap = cv2.VideoCapture(avipath)
        cnt = 0
        save_path = os.path.dirname(avipath) + '/'
        while True:
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.resize(img, self.save_size)
            os.makedirs(save_path + "val/", exist_ok=True)
            os.makedirs(save_path + "images/", exist_ok=True)
            if self.count % self.frame_interval == 0:
                if self.start_count < self.count:
                    if cnt % 10 == 0:
                        success, encoded_image = cv2.imencode('.bmp', img)
                        if success:
                            with open(save_path + "val/" + self.perfix + str(self.i) + self.save_img_format, 'wb') as f:
                                f.write(encoded_image)
                        # cv2.imwrite(save_path + "val/" + self.perfix + str(self.i) + self.save_img_format, img)
                        self.i += 1
                        cnt = 0
                    else:
                        success, encoded_image = cv2.imencode('.bmp', img)
                        if success:
                            with open(save_path + "images/" + self.perfix + str(self.i) + self.save_img_format, 'wb') as f:
                                f.write(encoded_image)
                        # cv2.imwrite(save_path + "images/" + self.perfix + str(self.i) + self.save_img_format, img)
                        self.i += 1
                    cnt += 1
                    if self.open_window:
                        img = self.add_progress(img, self.count, counts, None)
                        self.take_gui(img)
            self.count += 1

    # 鼠标响应回调函数
    def capture_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)
            self.position.append([x, y])

    # roi标点函数
    def mouse_roi(self, img):
        cv2.setMouseCallback("img", self.capture_event)
        if len(self.position) > 1:
            for i in range(0, len(self.position) - 1):
                cv2.line(img, self.position[i], self.position[i + 1], (255, 255, 255), 2)
        if len(self.position) == 4:
            cv2.line(img, self.position[3], self.position[0], (255, 255, 255), 2)
        dst = img[self.position[0][1]:self.position[2][1], self.position[0][0]:self.position[2][0]]
        cv2.imshow("dst", dst)

    def get_format(self):
        getformat = tk.Tk()
        getformat.geometry("400x300")
        getformat.title("选择处理格式")
        tk.Label(getformat, text="请输入你要处理的文件格式\n如’.jpg,.mp4‘可处理单个或多个格式\n关闭该窗口或输入空信息将使用默认格式\n"
                                 "视频默认格式为(‘.mp4’, ‘.avi’)\n其他文件默认格式为('.jpg', '.JPG', \n'.png', '.png', '.txt')", font=("Arial", 14)).pack(pady=10)
        format_entry = tk.Entry(getformat, width=30, font=("Arial", 12))
        format_entry.pack(pady=10)

        def on_submit():                                    # 创建提交按钮
            self.format = format_entry.get() if format_entry.get() else self.format
            try:
                self.format = tuple(i.strip(' ') for i in self.format.split(','))
            except:
                self.format = self.format
            getformat.destroy()                          # 关闭输入窗口
        tk.Button(getformat, text="提交", command=on_submit, width=20, bg="lightblue").pack(pady=10)
        getformat.wait_window()                          # 等待直到输入窗口关闭

    def set_save_video(self):
        set_window = tk.Tk()
        set_window.geometry("750x600")
        set_window.title("保存视频设置")
        tk.Label(set_window, text="因涉及本地路径，该窗口配置不可跳过！！！",
                 font=("Arial", 18)).grid(row=0, column=0, pady=10)
        tk.Label(set_window, text="需要保存的路径如(’C:/Pictures/work/txt/‘):", font=("Arial", 16)).grid(row=1, column=0, pady=10)
        save_path_entry = tk.Entry(set_window, width=30)
        save_path_entry.grid(row=1, column=1, pady=5)
        tk.Label(set_window, text="设置视频名字以及视频格式（默认'10.avi'）:", font=("Arial", 16)).grid(row=2, column=0, pady=5)
        video_name_entry = tk.Entry(set_window, width=30)
        video_name_entry.grid(row=2, column=1, pady=5)
        tk.Label(set_window, text="设置视频编码（默认'MPEG-4.avi'）:", font=("Arial", 16)).grid(row=3, column=0, pady=5)
        videoformat_entry = tk.Entry(set_window, width=30)
        videoformat_entry.grid(row=3, column=1, pady=5)
        tk.Label(set_window, text="设置视频帧率（默认'150'）:", font=("Arial", 16)).grid(row=4, column=0, pady=5)
        video_fps_entry = tk.Entry(set_window, width=30)
        video_fps_entry.grid(row=4, column=1, pady=5)
        tk.Label(set_window, text="设置视频大小（默认'1920,1200'）:", font=("Arial", 16)).grid(row=5, column=0, pady=5)
        video_size_entry = tk.Entry(set_window, width=30)
        video_size_entry.grid(row=5, column=1, pady=5)

        def on_submit():                                    # 创建提交按钮
            self.save_path = save_path_entry.get() if save_path_entry.get() else self.save_path
            self.video_name = video_name_entry.get() if video_name_entry.get() else self.video_name
            self.set_videoformat = videoformat_entry.get() if videoformat_entry.get() else self.set_videoformat
            self.save_video_fps = int(video_fps_entry.get()) if video_fps_entry.get() else self.save_video_fps
            self.save_size = tuple(int(i.strip(' ')) for i in video_size_entry.get().split(',')) if video_size_entry.get() else self.save_size
            set_window.destroy()                          # 关闭输入窗口
        tk.Button(set_window, text="提交", command=on_submit, width=20, bg="lightblue", font=("Arial", 16)).grid(row=6, column=0, columnspan=2, pady=10)

        tk.Label(set_window, text="视频编码参考:\n（注意：视频编码应与设置视频名字与格式时一致）\n'MPEG-4.mp4': MPEG-4编码的mp4视频格式\n"
                                  " 'H.264.mp4': H.264编码的mp4视频格式\n'YUV-4.avi': YUV-4编码的avi格式视频格式\n"
                                  "'MPEG-1.avi': MPEG-1编码的avi视频格式\n'MPEG-4.avi': MPEG-4编码的avi视频格式\n "
                                  "'OggVorbis.ogv': OggVorbis编码的ogv视频格式\n'Flash.flv': Flash编码的flv视频格式",
                 font=("Arial", 16)).grid(row=7, column=0, pady=10)
        set_window.wait_window()                          # 等待直到输入窗口关闭

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

# DataSet().roi_to_ground('C:/Users/HZY/Pictures/work/txt/,C:/Users/HZY/Pictures/work/ground/,C:/Users/HZY/Pictures/work/roi/')
# DataSet().connect_video('C:/Users/HZY/Pictures/work/txt/')

