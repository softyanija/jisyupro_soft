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
win = 2 #勝敗判定用のフラグ

root = tk.Tk()
root.title(u"curling")
root.geometry("1040x780")
display = tk.Canvas(root, width = win_width, height = win_height)
display.pack() #パック

cap = cv2.VideoCapture(1)

dictionary_name = cv2.aruco.DICT_4X4_50
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)



#
def camera_init():
    global cap
    
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (int(2*frame.shape[1]), int(2*frame.shape[0])))
        cv2.putText(frame, 'Please set marker', (140, 80), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.putText(frame, 'End : Space', (350,180), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.drawMarker(frame, (640,480), (0,0,255), markerType=cv2.MARKER_CROSS, markerSize=60, thickness=1, line_type=cv2.LINE_8)
        cv2.imshow('Camera Initialize', frame)
        
        k = cv2.waitKey(1)
        if k == 32:
            break

#枠組みを作る
def make_board():
    display.create_rectangle(40, 30, 40+640, 30+480,tag = "board")
    display.create_text(30, 40, text = "   ", font = ('FixedSys', 16), tag = "score")
    btn = tk.Button(display, text='判定', command = end_game)
    btn.place(x = 800, y = 550)
    btn2 = tk.Button(display, text='終了', command = root.destroy)
    btn2.place(x = 800, y = 700)
    
#石の座標を取得
def getmarkers(ids, corners):
    arr = np.empty((0,3))
    if ids is not None:
        for i, id in enumerate(ids):
            if i < 20:
                v = np.mean(corners[i][0],axis=0)
                arr = np.append(arr, np.array([[id[0], v[0], v[1]]]), axis=0)
    #print(arr)
    return arr

#石の座標の配列を取得しソート
def sort_stones(arr):
    center = np.array([x_center,y_center])
    buf_r = np.array([np.linalg.norm(arr[:,1:3] - center,axis = 1)]).reshape([arr.shape[0],1])
    buf_i = arr[:,0].reshape([arr.shape[0],1])
    ans = np.append(buf_i,buf_r,axis = 1)
    ans = ans[np.argsort(ans[:,1])]
    return ans

#盤面に石を表示、(x,y)は左上の座標
def board_stones(arr,x,y):
    r = 10
    display.delete("stones")
    if arr.any():
        for i in arr:
            display.create_oval(x+i[1]-r,y+i[2]+r,x+i[1]+r,y+i[2]-r,fill=str(id2color(i[0])), tag = "stones")
    
def show_stones(arr,x,y):#x,yは左上の座標
    d1 = 80
    d2 = 100 + d1
    display.delete("score")
    display.create_text(x, y, text = 'Rank', font = ('FixedSys', 20), tag = "score")
    display.create_text(x+d1, y, text = 'ID', font = ('FixedSys', 20), tag = "score")
    display.create_text(x+d2, y, text = 'Distance', font = ('FixedSys', 20), tag = "score")
    for i, st in enumerate(arr):
        display.create_text(x, y+40*(i+1), text = str(i+1), font = ('FixedSys', 20), tag = "score")
        display.create_text(x+d1, y+40*(i+1), text = str(int(st[0])), font = ('FixedSys', 20), tag = "score")
        display.create_text(x+d2, y+40*(i+1), text = str(int(st[1])), font = ('FixedSys', 20), tag = "score")
        
def id2color(id):
    if id//10:
        return 'blue'
    else:
        return 'red'
    
def winner(arr):
    global win
    if not arr.any():
        return 2
    else:
        return arr[0][0]//10

    
def end_game():
    global win
    if win == 0:
        display.create_text(360, 550, text = 'Red Win!', font = ('FixedSys', 40), tag = "winner")
    elif win == 1:
        display.create_text(360, 550, text = 'Blue Win!', font = ('FixedSys', 40), tag = "winner")
    else:
        display.create_text(360, 550, text = 'Draw', font = ('FixedSys', 40), tag = "winner")
    

#ゲームのメインループ
def gameloop():
    global dictionary, cap, test, win
    ret, frame = cap.read()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    stones = getmarkers(ids, corners)
    s_stones = sort_stones(test)
    win = winner(s_stones)
    board_stones(test,40,30)
    show_stones(s_stones,760,40)
    print(s_stones)
    root.after(tick, gameloop) #50ミリ秒経過後、ループの最初に戻る

    
#メイン部分
camera_init()
cv2.destroyAllWindows()
make_board()
test = np.array([[0, 380, 320],[1, 320, 240],[2, 100, 240],[10, 50, 240],[11, 160, 270],[12, 170, 360]])
#ゲームのメインループ
gameloop()
root.mainloop() #画面の表示
