import wheel.wheelfile
import zipfile
import tkinter as tk
import os

class DEcompress:
    def __init__(self):
        self.save_path = 'D:/MYproject/ZYscript/test/'
# 尝试解包安装.whl文件

    def decompress_package(self, path):
        self.save_path = path
        self.get_path()
        if os.path.isdir(path):
            for name in os.listdir(path):
                with zipfile.ZipFile(path+name, "r") as zip_ref:
                    zip_ref.extractall(self.save_path)
        else:
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(self.save_path)

    def get_path(self):
        getpath = tk.Tk()
        getpath.geometry("400x300")
        getpath.title("选择解压路径")
        tk.Label(getpath, text="请输入你要将其解压到何处\n如:C:/work/roi/\n已知情况下:\n该功能支持所有zip压缩原则的文件格式\n例如.zip,.tar,.whl等",
                 font=("Arial", 14)).pack(pady=10)
        format_entry = tk.Entry(getpath, width=30, font=("Arial", 12))
        format_entry.pack(pady=10)

        def on_submit():                                    # 创建提交按钮
            self.format = format_entry.get() if format_entry.get() else self.save_path
            getpath.destroy()                          # 关闭输入窗口
        tk.Button(getpath, text="提交", command=on_submit, width=20, bg="lightblue").pack(pady=10)
        getpath.wait_window()


# Decompress().decompress_package('20')

