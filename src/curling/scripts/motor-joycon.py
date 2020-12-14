#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import pygame
from pygame.locals import *
import time

angle1 = 180
angle2 = 90

class joyconController:
    def __init__(self):
        rospy.init_node('joycon_node', anonymous=True)
        self.motor_angle1_pub = rospy.Publisher('/servo_1', UInt16, queue_size=1)
        self.motor_angle2_pub = rospy.Publisher('/servo_2', UInt16, queue_size=1)
        rospy.Timer(rospy.Duration(0.1), self.timerCallback)
        pygame.joystick.init()
        self.joystick0 = pygame.joystick.Joystick(0)
        self.joystick0.init()
        self.joystickx = 0
        self.joysticky = 0
        pygame.init()

        global angle1
        global angle2

        # ボタンのカウントと速度の係数
        self.button_cnt = 0
        self.motor1 = 10
        self.motor2 = 10

        motor_angle1 = UInt16()
        motor_angle1.data = angle1
        self.motor_angle1_pub.publish(motor_angle1)
        motor_angle2 = UInt16()
        motor_angle2.data = angle2
        self.motor_angle2_pub.publish(motor_angle2)
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
        eventlist = pygame.event.get()
        global angle1
        global angle2
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
                    angle1 += self.motor1
                elif e.button==1:#右
                    angle1 -= self.motor1
                elif e.button==0:#下
                    angle1 = 0
                elif e.button==3:#上
                    angle1 = 140
                    motor_angle1.data = angle1
                    self.motor_angle1_pub.publish(motor_angle1)
                    rospy.sleep(2)

                    angle2 = 0
                    motor_angle2.data = angle2
                    self.motor_angle2_pub.publish(motor_angle2)
                    rospy.sleep(1)
                    
                    angle1 = 180
                    self.motor_angle1_pub.publish(motor_angle1)
        angle1 -= self.motor1*self.joystickx
        angle2 -= self.motor2*self.joysticky
        if angle1 < 0:
            angle1 = 0
        elif angle1 > 180:
            angle1 = 180

        if angle2 < 0:
            angle2 = 0
        elif angle2 > 180:
            angle2 = 180
            
        motor_angle1.data = angle1
        motor_angle2.data = angle2
        self.motor_angle1_pub.publish(motor_angle1)
        self.motor_angle2_pub.publish(motor_angle2)
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

