import os
import cv2
import numpy as np
import math
import random
import tkinter as tk
from tkinter import messagebox
from GetParameters import get_windowstate

class COPYPaste:
    def __init__(self):
        self.ROI_perfix = 'Background_'
        self.perfix = "ground_"
        self.isxywh = False
        self.get_img_format = '.jpg'
        self.format = None
        self.ground_size = [640, 384]
        self.ROI_size = [640, 384]
        # （1920， 1200）图片基准下（线条粗细基准，字体大小基准，字体y轴补偿）
        self.line_scale, self.text_scale, self.yawcompen_scale = 3, 1.5, 1.1
        self.open_window = False
        self.show_time = 1

    def ROI_buff(self, path):
        self.open_window, self.show_time = get_windowstate()
        path = [i.strip(' ') for i in path.split(',')]
        txtDir, baseground_path, ROIpath = path
        self.move_rockground(txtDir, baseground_path, ROIpath, 0)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "ROI_buff任务已完成")

    def ROI_armor(self, path):
        self.open_window, self.show_time = get_windowstate()
        path = [i.strip(' ') for i in path.split(',')]
        txtDir, baseground_path, ROIpath = path
        self.move_rockground(txtDir, baseground_path, ROIpath, 0)
        print("已完成ROI_armor任务")
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "ROI_armor任务已完成")

    def ROI_rock(self, path):
        self.open_window, self.show_time = get_windowstate()
        path = [i.strip(' ') for i in path.split(',')]
        txtDir, baseground_path, ROIpath = path
        self.move_rockground(txtDir, baseground_path, ROIpath, 1)
        print("已完成ROI_rock任务")
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "ROI_rock任务已完成")

    # 将某一ROI区域随机贴图到背景图中，路径要求3个文件夹路径
    def ROI_to_ground(self, path):
        self.open_window, self.show_time = get_windowstate()
        path = [i.strip(' ') for i in path.split(',')]
        txtDir, baseground_path, ROIpath = path
        count = 1
        for filename in os.listdir(txtDir):
            with open(txtDir + filename, 'rb') as f:
                img_array = np.frombuffer(f.read(), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
            # img = cv2.imread(txtDir + filename)
            random_name = os.listdir(baseground_path)[int(len(os.listdir(baseground_path))*random.random())]
            with open(baseground_path + random_name, 'rb') as f:
                img_array = np.frombuffer(f.read(), dtype=np.uint8)
            ground_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
            # ground_img = cv2.imread(baseground_path + random_name)
            img = cv2.resize(img, (int(ground_img.shape[1]/2), int(ground_img.shape[0]/2)))
            ground_img[int(ground_img.shape[0]/4):int(ground_img.shape[0]/4) + img.shape[0],
                       int(ground_img.shape[1]/4):int(ground_img.shape[1]/4) + img.shape[1]] = img
            # 注释代码为随机roi实例，供个人使用需求参考
            """random_point = [ground_img.shape[0]*random.random(), ground_img.shape[1]*random.random()]
            random_point[0] += (random_point[0] + img.shape[0] - ground_img.shape[0])\
                if (random_point[0] + img.shape[0] - ground_img.shape[0]) > 0 else 0
            random_point[1] += (random_point[1] + img.shape[1] - ground_img.shape[1])\
                if (random_point[1] + img.shape[1] -ground_img.shape[1]) > 0 else 0
            ground_img[random_point[0]:random_point[0] + img.shape[0],
                       random_point[1]:random_point[1] + img.shape[1]] = img"""
            # ground_img = cv2.resize(ground_img, self.save_size)
            success, encoded_image = cv2.imencode('.bmp', ground_img)
            if success:
                with open(ROIpath + "ground_" + filename, 'wb') as f:
                    f.write(encoded_image)
            # cv2.imwrite(ROIpath + "ground_" + filename, ground_img)
            if self.open_window:
                ground_img = self.add_progress(ground_img, count, len(os.listdir(txtDir)))
                count += 1
                self.take_gui(ground_img)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "ROI_to_ground任务已完成")

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

    def move_rockground(self, txtDir, groundpath, ROIpath, goal_type):
        self.get_format()
        if self.format:
            self.get_img_format = self.format
        txtNames = os.listdir(txtDir)
        count = 1
        for name in txtNames:
            if ('.txt' not in name) or (self.ROI_perfix in name):
                continue
            if name.endswith('.txt'):
                txtPath = os.path.join(txtDir, name)
                newLines = []
                all_line = []
                all_xywh = []
                with open(txtPath, 'r') as f:
                    for old_line in f.readlines():
                        old_line = old_line.strip().split()
                        all_line.extend(old_line)
                        all_xywh.extend(old_line[1:5])
                    if goal_type:
                        xywh = self.get_rectangle(all_xywh, 1)
                        line = [x for x in all_line if 0 < float(x) < 1]
                    else:
                        if not self.isxywh:
                            xywh = self.get_rectangle(all_line, 0)
                        line = all_line[1:]
                    for i in range(4):
                        line.insert(0, str(xywh[3-i]))
                    with open(txtPath.replace('.txt', self.get_img_format), 'rb') as f:
                        img_array = np.frombuffer(f.read(), dtype=np.uint8)
                    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                    # img = cv2.imread(txtPath.replace('.txt', self.get_img_format))
                    img = cv2.resize(img, self.ground_size)
                    line = np.array(line, dtype=np.float64).reshape(len(line) // 2, 2) * np.array([img.shape[1], img.shape[0]])
                    while True:
                        ROI_Scale = (np.random.random() * 0.2) + 1
                        if True not in ((line[0] - (line[1] * ROI_Scale * 0.5)) < [0] * 2) and True not in (
                                (line[0] + line[1] * ROI_Scale * 0.5) > self.ground_size):
                            break
                    newSize = (line[1] * ROI_Scale).astype(np.int64)                    # wh放缩尺寸
                    minpoint = line[0] - newSize * 0.5                                  # 最左上一点放缩后像素点
                    line[0] -= line[1] * 0.5                                            # 获取最左上一点放缩前像素点
                    if goal_type:
                        onesize = line[3] * ROI_Scale
                        twosize = line[int(len(line)/2+2)] * ROI_Scale
                    line[2:] = ((line[2:] - line[0]) / line[1]) * newSize + minpoint    # ROI放缩后各像素点
                    if goal_type:
                        line[3] = onesize
                        line[int(len(line)/2+2)] = twosize
                    randomint = int(np.random.randint(len(os.listdir(groundpath))))     # 从待选择背景中随机选择一张图片作为roi背景
                    with open(groundpath + os.listdir(groundpath)[randomint], 'rb') as f:
                        img_array = np.frombuffer(f.read(), dtype=np.uint8)
                    groundimg = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                    # groundimg = cv2.imread(groundpath + os.listdir(groundpath)[randomint])
                    groundimg = cv2.resize(groundimg, self.ground_size)
                    while True:
                        size_Scale = np.array(
                            [np.random.randint(-(self.ground_size[0] / 2), self.ground_size[0] / 2),
                             np.random.randint(-(self.ground_size[1] / 2), self.ground_size[1] / 2)])
                        if (True not in (minpoint + size_Scale < [0] * 2)) and (
                                True not in (minpoint + newSize + size_Scale > self.ground_size)):
                            break
                    groundline = line.copy()
                    groundline[0] = minpoint
                    groundline[1] = newSize
                    # 背景图待放ROI区域用放缩因子令其随机出现到图片中的任意位置
                    groundline += size_Scale
                    groundline[1] -= size_Scale
                    if goal_type:
                        groundline[3] -= size_Scale
                        groundline[int(len(line)/2+2)] -= size_Scale

                    groundpoint = groundline[:2].astype(np.int64)
                    linepoint = line[:2].astype(np.int64)
                    try:
                        # 将ROI区域贴到背景图中
                        groundimg[groundpoint[0][1]:groundpoint[0][1] + groundpoint[1][1],
                        groundpoint[0][0]:groundpoint[0][0] + groundpoint[1][0]] = \
                            cv2.resize(img[linepoint[0][1]:linepoint[0][1] + linepoint[1][1],
                                       linepoint[0][0]:linepoint[0][0] + linepoint[1][0]], newSize)
                        groundline[0] += groundline[1] / 2
                        newLine = sum((groundline / self.ground_size).tolist(), [])
                        if goal_type:
                            for i in range(4):
                                newLine.remove(newLine[0])
                            newLine.insert(int(len(newLine)/2), all_line[int(len(all_line)/2)])
                            for i in range(int((len(all_line)-len(newLine))/2)):
                                newLine.insert(6+i*3, all_line[7+i*3])
                                newLine.insert(int(len(newLine)/2+7+i*3), all_line[int(len(all_line)/2+7+i*3)])
                            newLines.append(" ".join(str(i) for i in [all_line[0]] + newLine[:int(len(newLine)/2)]))
                            newLines.append(" ".join(str(i) for i in [all_line[int(len(all_line)/2)]] + newLine[int(len(newLine)/2)+1:]))
                        else:
                            newLines.append(" ".join(str(i) for i in [all_line[0]] + newLine[4:]))
                    except:
                        continue
                save_path = os.path.join(ROIpath, self.ROI_perfix + str(name))
                os.makedirs(ROIpath, exist_ok=True)  # 创建文件夹
                with open(save_path, 'w') as f:
                    for newLine in newLines:
                        f.write(newLine + '\n')
                groundimg = cv2.resize(groundimg, self.ROI_size)
                success, encoded_image = cv2.imencode('.bmp', groundimg)
                if success:
                    with open(save_path.replace('.txt', self.get_img_format), 'wb') as f:
                        f.write(encoded_image)
                # cv2.imwrite(save_path.replace('.txt', self.get_img_format), groundimg)
                if self.open_window:
                    groundimg = self.add_progress(groundimg, count, len(os.listdir(txtDir)))
                    count += 1
                    self.take_gui(groundimg)

    # 添加工作进度条
    def add_progress(self, img, count, counts):
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
                    cv2.FONT_HERSHEY_DUPLEX, self.text_scale * img.shape[1] / 1920, (255, 255, 255),
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

    def take_gui(self, img):
        cv2.namedWindow("gui", cv2.WINDOW_NORMAL)
        cv2.imshow("gui", img)
        if cv2.waitKey(self.show_time) == 27:
            self.open_window = False
            cv2.destroyAllWindows()

# COPYPaste().ROI_rock('C:/Users/HZY/Pictures/work/txt/,C:/Users/HZY/Pictures/work/ground/,C:/Users/HZY/Pictures/work/roi/')
# C:/Users/HZY/Pictures/work/txt/, C:/Users/HZY/Pictures/work/ground/, C:/Users/HZY/Pictures/work/roi/
# COPYPaste().ground_to_label('C:/Users/HZY/Pictures/work/txt/')


