__author__ = 'wing2048'
import pygame
pygame.init()
font = pygame.font.SysFont('Courier', 25)
smooth_move_amount = 1
move_amount = 0.5
YAW_INDICATOR_CENTER = (360, 50)
PITCH_INDICATOR_CENTER = (130, 150)
FRICTION_CONSTANT = 0.8
TOUCH_ACCURACY = 20
TOP_ARM_LENGTH = 30
MIDDLE_ARM_LENGTH = 40
BOTTOM_ARM_LENGTH = 50
LIGHT_ANGLE = 10
