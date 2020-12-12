#!/usr/bin/env python
# coding: UTF-8
import sys
import Tkinter as tk
import cv2
import numpy as np

win_width = 960+40*2
win_height = 720+30*2
tick = 40
x_center = 320
y_center = 240

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
    #print(arr)
    return arr

#石の座標の配列を取得しソートして、画面に表示
def show_stones(arr, x, y):#(x,y)は左上の座標
    center = np.array([x,y])
    buf_r = np.array([np.linalg.norm(arr[:,1:3] - center,axis = 1)]).reshape([arr.shape[0],1])
    buf_i = arr[:,0].reshape([arr.shape[0],1])
    ans = np.append(buf_i,buf_r,axis = 1)
    return ans
    
#ゲームのメインループ
def gameloop():
    global dictionary, cap
    ret, frame = cap.read()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    stones = getmarkers(ids, corners)
    stones = show_stones(stones,320, 240)
    print(stones)
    root.after(tick, gameloop) #50ミリ秒経過後、ループの最初に戻る

    
#メイン部分
init()

#ゲームのメインループ
gameloop()
root.mainloop() #画面の表示
