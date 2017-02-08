from __future__ import division
import pygame
from geometry_msgs.msg import Twist
import rospy
import sys

pygame.init()
win_x =1000
win_y = 800 
pygame.display.set_mode((win_x, win_y))

pygame.key.set_repeat(100, 100)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=2)
rospy.init_node('vel', anonymous=True)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    pygame.event.poll()
    pressed = pygame.key.get_pressed()
    lin_vel = 0
    ang_vel = 0

    if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            lin_vel += 0.2
    if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            lin_vel -= 0.2
    if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            ang_vel -= 0.3
    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            ang_vel += 0.3
    if pygame.mouse.get_pressed()[0]:
            lin = pygame.mouse.get_pos()[1]
            ang = pygame.mouse.get_pos()[0]
            lin = -(lin-win_y/2)/win_y
            ang = -(ang-win_x/2)/win_x
            lin_vel = lin
	    ang_vel = ang

    print 'cmd', lin_vel, ang_vel
    twist = Twist()
    twist.linear.x = lin_vel
    twist.angular.z = ang_vel
    pub.publish(twist)
    rate.sleep()
