import os
import json
import numpy as np
import math
import cv2
import tkinter as tk
from tkinter import messagebox, filedialog
from GetParameters import get_windowstate
from PIL import Image


class Format:
    def __init__(self, ):
        self.imgSize = (1920, 1200)
        self.perfix = "ground_"
        self.get_img_format = ('.jpg', '.png', '.bmp')
        self.get_swap = 'ico'
        self.format = ('.jpg', '.png', '.bmp')
        self.save_path = None
        self.save_img_format = '.bmp'
        # （1920， 1200）图片基准下（线条粗细基准，字体大小基准，字体y轴补偿）
        self.line_scale, self.text_scale, self.yawcompen_scale = 3, 1.5, 1.1
        self.open_window = False
        self.show_time = 0
        self.ico_size = 256
        self.get_entry_path = {}

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
            try:
                if self.open_window:
                    with open('./_internal/win.jpg', 'rb') as f:
                        img_array = np.frombuffer(f.read(), dtype=np.uint8)
                    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                    img = self.add_progress(img, count, len(os.listdir(path)), 1)
                    count += 1
                    self.take_gui(img)
            except:
                messagebox.showinfo('警告', "本地计算机不支持在本地部署可视化进度，请联系管理员获取可视化视图。")
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
            try:
                if self.open_window:
                    with open('./_internal/win.jpg', 'rb') as f:
                        img_array = np.frombuffer(f.read(), dtype=np.uint8)
                    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                    img = self.add_progress(img, count, len(os.listdir(path)), 1)
                    count += 1
                    self.take_gui(img)
            except:
                messagebox.showinfo('警告', "本地计算机不支持在本地部署可视化进度，请联系管理员获取可视化视图。")
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
                try:
                    if self.open_window:
                        with open('./_internal/win.jpg', 'rb') as f:
                            img_array = np.frombuffer(f.read(), dtype=np.uint8)
                        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
                        img = self.add_progress(img, count, len(os.listdir(path)), 1)
                        count += 1
                        self.take_gui(img)
                except:
                    messagebox.showinfo('警告', "本地计算机不支持在本地部署可视化进度，请联系管理员获取可视化视图。")
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "label_cut_xywh任务已完成")

    def image_swap_ico(self, path):
        self.ico_size = 256
        self.get_entry_path = {}
        self.open_window, self.show_time = get_windowstate()
        count = 0
        self.get_format()
        self.set_swap()
        if os.path.isdir(path):
            for name in os.listdir(path):
                if name.endswith(self.format):
                    if self.get_swap == 'ico':
                        self.image_to_ico(os.path.join(path, name), name.split('.')[0], count, len(os.listdir(path)))
                    else:
                        self.ico_to_image(os.path.join(path, name), name.split('.')[0], count, len(os.listdir(path)))
        else:
            if self.get_swap == 'ico':
                self.image_to_ico(path, os.path.splitext(os.path.basename(path))[0], count, 1)
            else:
                self.ico_to_image(path, os.path.splitext(os.path.basename(path))[0], count, 1)
        cv2.destroyAllWindows()
        messagebox.showinfo('温馨提示', "image_swap_ico任务已完成")

    def ico_to_image(self, path, name, count, counts):
        image = Image.open(path)  # 读取ICO文件
        image = image.convert("RGB")  # 转换为 RGB 格式（防止透明通道问题）
        img = np.array(image)  # 转换为 OpenCV 格式
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # PIL是RGB，OpenCV需要BGR
        img = cv2.resize(img, self.ico_size)
        success, encoded_image = cv2.imencode(self.save_img_format, img)
        if success:
            with open(f'{self.save_path}/{name}{self.save_img_format}', 'wb') as f:
                f.write(encoded_image)
        if self.open_window:
            img = self.add_progress(img, count, counts, None)
            count += 1
            self.take_gui(img)

    def image_to_ico(self, path, name, count, counts):
        image = Image.open(path).convert("RGBA")
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))        # 创建白色背景
        image = Image.alpha_composite(background, image)                        # 合并图片
        image.save(f'{self.save_path}/{name}.ico', format="ICO", sizes=self.ico_size)                     # 保存 ICO
        with open(path, 'rb') as f:
            img_array = np.frombuffer(f.read(), dtype=np.uint8)
        dst = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 解析图片数据
        if self.open_window:
            dst = self.add_progress(dst, count, counts, None)
            count += 1
            self.take_gui(dst)

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
        tk.Label(getformat, text="请输入你要处理的文件格式\n如’.jpg‘或’.png‘,'.ico'等\n关闭该窗口或输入空信息将使用默认格式\n"
                                 "默认格式:'.jpg', 'png', 'bmp'", font=("Arial", 14)).pack(pady=10)
        format_entry = tk.Entry(getformat, width=30, font=("Arial", 12))
        format_entry.pack(pady=10)

        def on_submit():                                    # 创建提交按钮
            self.format = format_entry.get() if format_entry.get() else self.format
            try:
                self.format = tuple(i.strip(' ') for i in self.format.split(','))
            except:
                self.format = self.format
            getformat.destroy()                          # 关闭输入窗口
        tk.Button(getformat, text="提交", command=on_submit, width=15, font=("Arial", 16), bg="lightblue").pack(pady=10)
        getformat.wait_window()

    def set_swap(self):
        setswap = tk.Tk()
        setswap.geometry("500x400")
        setswap.title("转换设置")
        tk.Label(setswap, text="因涉及本地路径,该窗口不可跳过!", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10, padx=0)
        tk.Label(setswap, text="输入要保存的路径:", font=("Arial", 16)).grid(row=1, column=0, pady=10, padx=0)
        save_path_entry = tk.Entry(setswap, width=20, font=("Arial", 15))
        save_path_entry.grid(row=1, column=1, pady=10, padx=0)
        self.get_entry_path['save_path'] = save_path_entry
        tk.Button(setswap, text="浏览", command=lambda: self.select_path('save_path'), width=10, bg="lightblue",
                  font=("Arial", 14)).grid(row=2, column=1, pady=0, padx=0)
        tk.Label(setswap, text="输入要获得的格式:", font=("Arial", 16)).grid(row=3, column=0, pady=10, padx=0)
        save_img_entry = tk.Entry(setswap, width=20, font=("Arial", 15))
        save_img_entry.grid(row=3, column=1, pady=10, padx=0)
        tk.Label(setswap, text="获得的文件大小(默认256):", font=("Arial", 16)).grid(row=4, column=0, pady=10, padx=0)
        ico_size_entry = tk.Entry(setswap, width=20, font=("Arial", 15))
        ico_size_entry.grid(row=4, column=1, pady=10, padx=0)
        tk.Label(setswap, text="图标文件一般为(单个数字)32,128,256。\n图片文件一般为(2个数字用逗号隔开)1920,1280", font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=10, padx=0)

        def on_submit():                                    # 创建提交按钮
            self.save_path = save_path_entry.get() if save_path_entry.get() else None
            self.save_img_format = save_img_entry.get() if save_img_entry.get() else None
            self.ico_size = ico_size_entry.get() if ico_size_entry.get() else self.ico_size
            if self.save_img_format == '.ico':
                self.get_swap = 'ico'
                self.ico_size = [(int(self.ico_size), int(self.ico_size))]
            else:
                self.get_swap = 'img'
                self.ico_size = (int(self.ico_size.split(',')[0]), int(self.ico_size.split(',')[1]))
            setswap.destroy()                          # 关闭输入窗口
        tk.Button(setswap, text="提交", command=on_submit, width=15, font=("Arial", 16), bg="lightblue").grid(row=6, column=0, columnspan=2, pady=10)
        setswap.wait_window()                          # 等待直到输入窗口关闭

    def select_path(self, entry_name):
        # if entry_name == 'desktop_path':
        folder_selected = filedialog.askdirectory()  # 打开文件夹选择对话框
        # else:
        #     folder_selected = filedialog.askopenfilename()  # 打开文件夹选择对话框
        if folder_selected:
            self.get_entry_path[entry_name].delete(0, tk.END)  # 清空已有内容
            self.get_entry_path[entry_name].insert(0, folder_selected)  # 插入选定路径

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
# Format().image_swap_ico('D:/MYproject/ZYscript/test/')
# Format().set_swap()
