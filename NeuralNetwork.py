import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector                  # 脸部
from tkinter import messagebox
import tkinter as tk


class Network:
    def __init__(self):
        self.size = [1280, 720]
        self.permission = False

    def identify_hand(self, flag):
        self.ask_permission()
        if self.permission:
            try:
                detector = HandDetector(detectionCon=0.8, maxHands=2)
                cap = cv2.VideoCapture(0)
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
                cap = cv2.VideoCapture(0)
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
        askpermission = tk.Tk()
        askpermission.geometry("400x200")
        askpermission.title("权限请求")
        tk.Label(askpermission, text="此功能将启用你的摄像头,\n并访问你的电脑相机信息,\n是否允许系统获取您的相机权限:", font=("Arial", 18)).pack(pady=10)

        def yes_submit():
            self.permission = True
            askpermission.destroy()

        def no_submit():
            self.permission = False
            askpermission.destroy()

        tk.Button(askpermission, text="否(NO)", command=no_submit, width=10, font=("Arial", 16), bg="lightblue").pack(side=tk.LEFT, pady=10, padx=10)
        tk.Button(askpermission, text="是(YES)", command=yes_submit, width=10, font=("Arial", 16), bg="lightblue").pack(side=tk.RIGHT, pady=10, padx=10)
        askpermission.wait_window()


# Network().ask_permission()

