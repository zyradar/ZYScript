import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector                  # 脸部
from tkinter import messagebox
import tkinter as tk


class Network:
    def __init__(self):
        self.size = [1280, 720]
        self.permission = False
        self.camera_id = None

    def identify_hand(self, flag):
        self.ask_permission()
        if self.permission:
            try:
                detector = HandDetector(detectionCon=0.8, maxHands=2)
                cap = cv2.VideoCapture(self.camera_id)
                cap.set(3, self.size[0])
                cap.set(4, self.size[1])
                while cv2.waitKey(1) != 27:
                    ret, img = cap.read()
                    hands, img = detector.findHands(img, draw=True)
                    if hands:
                        x, y, w, h = hands[0]['bbox']   # 左上点和宽高
                        length, info, img = detector.findDistance((x, y), (x+w, y+h), img)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.imshow("img", img)
                messagebox.showwarning('温馨提示', "identify_hand任务已完成")
            except:
                messagebox.showwarning('警告!!!', '找不到摄像头设备，请检查电脑是否开启摄像头或电脑是否拥有摄像头设备')
        else:
            messagebox.showwarning('温馨提示', "因未能获取相机权限,identify_hand任务中止")

    def identify_face(self, flag):
        self.ask_permission()
        if self.permission:
            try:
                detector = FaceMeshDetector()
                cap = cv2.VideoCapture(self.camera_id)
                cap.set(3, self.size[0])
                cap.set(4, self.size[1])
                while cv2.waitKey(1) != 27:
                    ret, img = cap.read()
                    img, faces = detector.findFaceMesh(img, draw=True)
                    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                    cv2.imshow("img", img)
                messagebox.showwarning('温馨提示', "identify_face任务已完成")
            except:
                messagebox.showwarning('警告!!!', '找不到摄像头设备，请检查电脑是否开启摄像头或电脑是否拥有摄像头设备')
        else:
            messagebox.showwarning('温馨提示', "因未能获取相机权限,identify_face任务中止")

    def ask_permission(self):
        root = tk.Tk()
        root.geometry("500x400")
        root.title("权限请求")
        askpermission = tk.Frame(root)
        askpermission.pack()
        tk.Label(askpermission, text="此功能将启用你的摄像头,\n并访问你的电脑相机信息,\n是否允许系统获取您的相机权限:", font=("Arial", 18)).pack(pady=20)

        def yes_submit():
            self.permission = True
            try:
                cameras = self.detecting_camera()
            except:
                self.permission = False
                cameras = None
                messagebox.showwarning('警告!!!', '经系统检测，启用开系统时未启用管理员权限，被本地计算机禁止访问相机设备')
                root.destroy()
            if cameras:
                selectcamera = tk.Frame(root)
                askpermission.pack_forget()
                selectcamera.pack()
                tk.Label(selectcamera, text=f"已检测到本地计算机共有{len(cameras)}个相机设备。", font=("Arial", 18)).pack(pady=0)
                tk.Label(selectcamera, text=f"请选择你要使用的相机设备：", font=("Arial", 18)).pack(pady=0)

                def select_camera(id):
                    self.camera_id = id
                    root.destroy()

                for i in range(len(cameras)):
                    tk.Button(selectcamera, text=f"相机{i}", command=lambda id=i: select_camera(id), width=10, font=("Arial", 18),
                              bg="lightblue").pack(pady=5)
            else:
                messagebox.showwarning('警告!!!', '无法检测到摄像头设备，请确认计算机是否拥有相机设备')

        def no_submit():
            self.permission = False
            root.destroy()

        tk.Button(askpermission, text="否(NO)", command=no_submit, width=10, font=("Arial", 18), bg="lightblue").pack(side=tk.LEFT, pady=10, padx=30)
        tk.Button(askpermission, text="是(YES)", command=yes_submit, width=10, font=("Arial", 18), bg="lightblue").pack(side=tk.RIGHT, pady=10, padx=30)
        askpermission.wait_window()

    def detecting_camera(self, max_devices=10):
        available_cameras = []
        for index in range(max_devices):
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)  # CAP_DSHOW 适用于 Windows，可加快检测速度
            if cap.isOpened():
                available_cameras.append(index)
                cap.release()  # 释放摄像头资源
        return available_cameras


# Network().identify_hand(7)

