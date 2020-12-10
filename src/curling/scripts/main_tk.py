#!/usr/bin/env python
# coding: UTF-8
import sys
import Tkinter as tk

win_width = 960+40*2
win_height = 720+30*2
tick = 40

root = tk.Tk()
root.title(u"curling")
root.geometry("1040x780")
cv = tk.Canvas(root, width = win_width, height = win_height)
cv.pack() #パック

#枠組みを作る
def init():
    cv.create_rectangle(40, 30, 40+640, 30+480,tag = "board")

#ゲームのメインループ
def gameloop():
    root.after(tick, gameloop) #50ミリ秒経過後、ループの最初に戻る

    
#メイン部分
init()
root.mainloop() #画面の表示
