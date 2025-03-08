import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceMeshModule import FaceMeshDetector                  # 脸部
from tkinter import messagebox


class Network:
    def __init__(self):
        self.size = [1280, 720]

    def identify_hand(self, flag):
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
        except:
            messagebox.showwarning('警告!!!', '找不到摄像头设备，请检查电脑是否开启摄像头或电脑是否拥有摄像头设备')

    def identify_face(self, flag):
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
        except:
            messagebox.showwarning('警告!!!', '找不到摄像头设备，请检查电脑是否开启摄像头或电脑是否拥有摄像头设备')


# Network().get_face()

