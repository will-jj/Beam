from __future__ import division
import pygame
from geometry_msgs.msg import Twist
import rospy
import sys

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
STYLISH = (245, 255, 250)
pygame.init()
win_x =2000
win_y = 1000 



screen = pygame.display.set_mode((win_x, win_y))
screen.fill(STYLISH)

pygame.key.set_repeat(100, 100)
pygame.draw.line(screen, BLACK, [win_x/2, 0], [win_x/2,win_y], 5)
pygame.draw.line(screen, BLACK, [0, win_y/2], [win_x,win_y/2], 5)
myfont = pygame.font.SysFont("monospace", 15)

# render text
label = myfont.render("Angular Velocity", 1, (BLACK))
label2 = myfont.render("Linear Velocity", 1, (BLACK))
label2 = pygame.transform.rotate(label2, 90)
screen.blit(label, (win_x//2 +win_x//20,win_y//2-win_y//20))
screen.blit(label2, (win_x//2 -win_x//20,win_y//2-win_y//5))
pygame.display.flip()
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
