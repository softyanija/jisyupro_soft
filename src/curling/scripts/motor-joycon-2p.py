#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import pygame
from pygame.locals import *
import time

angle1 = 0
angle2 = 90
angle3 = 0
angle4 = 90
f = 0
l = 1 #LED
red = 255
blue = 255

class joyconController:
    def __init__(self):
        rospy.init_node('joycon_node', anonymous=True)
        self.motor_angle1_pub = rospy.Publisher('/servo_1', UInt16, queue_size=1)
        self.motor_angle2_pub = rospy.Publisher('/servo_2', UInt16, queue_size=1)
        self.motor_angle3_pub = rospy.Publisher('/servo_3', UInt16, queue_size=1)
        self.motor_angle4_pub = rospy.Publisher('/servo_4', UInt16, queue_size=1)
        self.LED_red_pub = rospy.Publisher('/LED_red', UInt16, queue_size=1)
        self.LED_blue_pub = rospy.Publisher('/LED_blue', UInt16, queue_size=1)
        rospy.Timer(rospy.Duration(0.1), self.timerCallback)
        pygame.joystick.init()
        self.joystick0 = pygame.joystick.Joystick(0)
        self.joystick0.init()
        self.joystickx = 0
        self.joysticky = 0
        pygame.init()

        global angle1
        global angle2
        global angle3
        global angle4
        global l

        # ボタンのカウントと速度の係数
        self.button_cnt = 0
        self.motor1 = 10
        self.motor2 = 2
        self.motor3 = 10
        self.motor4 = 2

        motor_angle1 = UInt16()
        motor_angle1.data = angle1
        self.motor_angle1_pub.publish(motor_angle1)
        motor_angle2 = UInt16()
        motor_angle2.data = angle2
        self.motor_angle2_pub.publish(motor_angle2)

        motor_angle3 = UInt16()
        motor_angle3.data = angle3
        self.motor_angle3_pub.publish(motor_angle3)
        motor_angle4 = UInt16()
        motor_angle4.data = angle4
        self.motor_angle2_pub.publish(motor_angle4)

        LED_red = UInt16()
        LED_red.data = 128
        self.LED_red_pub.publish(LED_red)
        LED_blue = UInt16()
        LED_blue.data = 128
        self.LED_blue_pub.publish(LED_blue)
        '''
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.twist_pub.publish(twist)
        print 
        print '▲ : UP Linear X,  ▼ : DOWN Linear X'
        print '◀ : UP Angular Z, ▶ : DOWN Angular Z'
        print
        '''
        
    def timerCallback(self, event):
        motor_angle1 = UInt16()
        motor_angle2 = UInt16()
        motor_angle3 = UInt16()
        motor_angle4 = UInt16()
        LED_red = UInt16()
        LED_blue = UInt16()
        eventlist = pygame.event.get()
        global angle1
        global angle2
        global angle3
        global angle4
        global f
        global l
        global red
        global blue

        if f == 0:
            # イベント処理
            for e in eventlist:
                if e.type == QUIT:
                    return
                # スティックの処理
                if e.type == pygame.locals.JOYHATMOTION:
                    self.button_cnt += 1
                    self.joystickx, self.joysticky = self.joystick0.get_hat(0)
                    # ボタンの処理
                elif e.type == pygame.locals.JOYBUTTONDOWN:
                    self.button_cnt += 1
                    if e.button==2:#左
                        f = 1
                    elif e.button==1:#右
                        f = 1
                    elif e.button==0:#下
                        angle1 = 0
                    elif e.button==3:#上
                        angle1 = 20
                        motor_angle1.data = angle1
                        self.motor_angle1_pub.publish(motor_angle1)
                        rospy.sleep(1)
                    
                        angle1 = 0
                        self.motor_angle1_pub.publish(motor_angle1)
            angle2 -= self.motor2*self.joystickx
            
            if angle1 < 0:
                angle1 = 0
            elif angle1 > 20:
                angle1 = 20

            if angle2 < 40:
                angle2 = 0
            elif angle2 > 140:
                angle2 = 140

            red = 255
            blue = 0
            
        else:
            # イベント処理
            for e in eventlist:
                if e.type == QUIT:
                    return
                # スティックの処理
                if e.type == pygame.locals.JOYHATMOTION:
                    self.button_cnt += 1
                    self.joystickx, self.joysticky = self.joystick0.get_hat(0)
                    # ボタンの処理
                elif e.type == pygame.locals.JOYBUTTONDOWN:
                    self.button_cnt += 1
                    if e.button==2:#左
                        f = 0
                    elif e.button==1:#右
                        f = 0
                    elif e.button==0:#下
                        angle3 = 0
                    elif e.button==3:#上
                        angle3 = 20
                        motor_angle3.data = angle3
                        self.motor_angle3_pub.publish(motor_angle3)
                        rospy.sleep(1)
                    
                        angle3 = 0
                        self.motor_angle3_pub.publish(motor_angle3)
            angle4 -= self.motor4*self.joystickx
            
            if angle3 < 0:
                angle3 = 0
            elif angle3 > 20:
                angle3 = 20

            if angle4 < 50:
                angle4 = 50
            elif angle4 > 160:
                angle4 = 160

            red = 0
            blue = 255
            
                
            
        motor_angle1.data = angle1
        motor_angle2.data = angle2
        motor_angle3.data = angle3
        motor_angle4.data = angle4
        LED_red.data = red
        LED_blue.data = blue
        self.motor_angle1_pub.publish(motor_angle1)
        self.motor_angle2_pub.publish(motor_angle2)
        self.motor_angle3_pub.publish(motor_angle3)
        self.motor_angle4_pub.publish(motor_angle4)
        self.LED_red_pub.publish(LED_red)
        self.LED_blue_pub.publish(LED_blue)
        print self.joystickx
'''

        self.twist_pub.publish(twist)

        if self.button_cnt>=10:
            print 
            print '▲ : UP Linear X,  ▼ : DOWN Linear X'
            print '◀ : UP Angular Z, ▶ : DOWN Angular Z'
            print
            self.button_cnt = 0
        
'''
'''
def face_detection_cb(msg):
    pub = rospy.Publisher('motor1/command', Int64, queue_size=1)

    motor_command_msg = Int64()
    face_pos = [0, 0]
    global motor_angle

    # face check
    if len(msg.faces):
        face = msg.faces[0].face
        face_pos[0] = face.x
        face_pos[1] = face.y
        # check face position. left or right
        if face_pos[0] <= image_center[0]:
            motor_angle -= 1
        else:
            motor_angle += 1

        motor_command_msg.data = motor_angle

        # print
        print "face_pos(x, y): ({} {})".format(face_pos[0], face_pos[1])
        print "/motor1/command: {}\n".format(motor_command_msg.data)

        # publish
        pub.publish(motor_command_msg)
    else:
        print "no faces"
'''
    
'''
def main():
    rospy.init_node('motor_command_by_face', anonymous=True)
    rospy.Subscriber('face_detection/faces', FaceArrayStamped, face_detection_cb)
    rate =  rospy.Rate(10)
    
    rospy.spin()
    rate.sleep()
'''

if __name__ == '__main__':
    try:
        jc = joyconController()
        rospy.spin()
    except pygame.error:
        print 'joystickが見つかりませんでした。'

