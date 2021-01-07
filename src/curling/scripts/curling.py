#!/usr/bin/env python
# coding: UTF-8
import sys
import Tkinter as tk
import cv2
import numpy as np
bi = 1.5
win_width = int((960+40*2)*bi)
win_height = int((600+30*2)*bi)
tick = int(40*bi)
x_center = int(320*bi)
y_center = int(240*bi)
win = 2 #勝敗判定用のフラグ
sc = 1 #表示内容のフラグ
root = tk.Tk()
root.title("curling")
root.geometry("1560x990")
display = tk.Canvas(root, width = win_width, height = win_height)
display.pack() #パック

cap = cv2.VideoCapture(1)

dictionary_name = cv2.aruco.DICT_4X4_50
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)

def e(n):
    global bi
    return int(n*bi)

#カメラの設定
def camera_init():
    global cap    
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (int(2*frame.shape[1]), int(2*frame.shape[0])))
        cv2.putText(frame, 'Please set marker', (140, 80), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.putText(frame, 'End : Space', (350,180), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5, cv2.LINE_AA)
        cv2.drawMarker(frame, (640, 480), (0,0,255), markerType=cv2.MARKER_CROSS, markerSize=60, thickness=1, line_type=cv2.LINE_8)
        cv2.imshow('Camera Initialize', frame)
        
        k = cv2.waitKey(1)
        if k == 32:
            break

#枠組みを作る
def make_board():
    r = 3*640/23/2
    display.create_rectangle(0, 0, e(1040), e(780), fill = "white",tag = "board")
    display.create_rectangle(e(40), e(30), e(40+640), e(30+480), fill = "BurlyWood",tag = "board")
    display.create_text(e(30), e(40), text = "   ", font = ('FixedSys', e(16)), tag = "score")
    display.create_oval(e(360-r),e(270-r),e(360+r),e(270+r), tag = "board")
    display.create_oval(e(360-2*r),e(270-2*r),e(360+2*r),e(270+2*r), tag = "board")
    display.create_oval(e(360-3*r),e(270-3*r),e(360+3*r),e(270+3*r), tag = "board")
    
    btn3 = tk.Button(display, text='ID', font = ('FixedSys', e(30), 'bold'), command = change_view)
    btn3.place(x = e(700), y = e(550))
    btn = tk.Button(display, text='判定', font = ('FixedSys', e(30), 'bold'), command = end_game)
    btn.place(x = e(785), y = e(550))
    btn2 = tk.Button(display, text='終了', font = ('System', e(30), 'bold'), command = root.destroy)
    btn2.place(x = e(910), y = e(550))
    
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
    center = np.array([320,240])
    buf_r = np.array([np.linalg.norm((arr[:,1:3] - center)*23/640,axis = 1)]).reshape([arr.shape[0],1])
    buf_i = arr[:,0].reshape([arr.shape[0],1])
    ans = np.append(buf_i,buf_r,axis = 1)
    ans = ans[np.argsort(ans[:,1])]
    return ans

#盤面に石を表示、(x,y)は左上の座標
def board_stones(arr,x,y):
    r = 3.2*640/23/2
    display.delete("stones")
    global sc
    if arr.any():
        for i in arr:
            display.create_oval(e(x+i[1]-r),e(y+i[2]+r),e(x+i[1]+r),e(y+i[2]-r),fill=str(id2color(i[0])), tag = "stones")
            if sc == -1:
                display.create_text(e(i[1]+0.9*r), e(i[2]+0.6*r), text = int(i[0])%10, font = ('FixedSys', e(40)), tag = "stones")
                print("hoge")

#石の情報を表示、x,yは左上の座標
def show_stones(arr,x,y):
    display.delete("score")
    d1 = 90
    d2 = 120 + d1
    display.create_text(e(x), e(y), text = 'Rank', font = ('FixedSys', e(23)), tag = "score")
    display.create_text(e(x+d1), e(y), text = 'Color', font = ('FixedSys', e(23)), tag = "score")
    display.create_text(e(x+d2), e(y), text = 'Distance', font = ('FixedSys', e(23)), tag = "score")
    for i, st in enumerate(arr):
        if i < 10:
            display.create_text(e(x), e(y+40*(i+1)), text = str(i+1), font = ('FixedSys', e(23)), tag = "score")
            
            if sc == 1:
                display.create_text(e(x+d1), e(y+40*(i+1)), text = id2color(st[0]), font = ('FixedSys', e(23)), tag = "score")
                display.create_text(e(x+d2), e(y+40*(i+1)), text = str(int(10*st[1])/float(10)), font = ('FixedSys', e(23)), tag = "score")
            else:
                display.create_text(e(x+d1), e(y+40*(i+1)), text = id2color(st[0])+str(int(st[0])%10), font = ('FixedSys', e(23)), tag = "score")
            
                display.create_text(e(x+d2), e(y+40*(i+1)), text = str(int(10*st[1])/float(10)), font = ('FixedSys', e(23)), tag = "score")

        
def id2color(id):
    if id//10:
        return 'Blue'
    else:
        return 'Red'
    
def winner(arr):
    global win
    if not arr.any():
        return 2
    else:
        return arr[0][0]//10

def change_view():
    global sc
    sc *= -1

def end_game():
    global win
    display.delete("winner")
    if win == 0:
        display.create_text(e(360), e(570), text = 'Red Win!', fill = 'red', font = ('FixedSys', e(70)), tag = "winner")
    elif win == 1:
        display.create_text(e(360), e(570), text = 'Blue Win!', fill = 'blue', font = ('FixedSys', e(70)), tag = "winner")
    else:
        display.create_text(e(360), e(570), text = 'Draw', font = ('FixedSys', e(70)), tag = "winner")
    

#ゲームのメインループ
def gameloop():
    global dictionary, cap, test, win
    ret, frame = cap.read()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    stones = getmarkers(ids, corners)
    s_stones = sort_stones(stones)
    win = winner(s_stones)
    board_stones(stones,40,30)
    show_stones(s_stones,743,40)
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
