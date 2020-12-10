#!/usr/bin/env python
# coding: UTF-8
import sys
import Tkinter as tk
import cv2
import numpy as np

win_width = 960+40*2
win_height = 720+30*2
tick = 40

root = tk.Tk()
root.title(u"curling")
root.geometry("1040x780")
display = tk.Canvas(root, width = win_width, height = win_height)
display.pack() #パック

cap = cv2.VideoCapture(0)

dictionary_name = cv2.aruco.DICT_4X4_50
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)




#枠組みを作る
def init():
    display.create_rectangle(40, 30, 40+640, 30+480,tag = "board")
    
#石の座標を取得
def getmarkers(ids, corners):
    arr = np.empty((0,3))
    if ids is not None:
        for i, id in enumerate(ids):
            v = np.mean(corners[i][0],axis=0)
            arr = np.append(arr, np.array([[id[0], v[0], v[1]]]), axis=0)
            #print([id[0], v[0], v[1]])
    print(arr)

    
#ゲームのメインループ
def gameloop():
    global dictionary, cap
    ret, frame = cap.read()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    getmarkers(ids, corners)
    root.after(tick, gameloop) #50ミリ秒経過後、ループの最初に戻る

    
#メイン部分
init()

#ゲームのメインループ
gameloop()
root.mainloop() #画面の表示
