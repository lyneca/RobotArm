import math

import serial
import pygame


move_amount = 1
__author__ = 'wing2048'
YAW_INDICATOR_CENTER = (600, 400)
PITCH_INDICATOR_CENTER = (300, 400)


class Servo():
    def __init__(self, servo_id):
        self.id = servo_id
        self.angle = 0

    def set_angle(self, angle):
        self.angle = angle


class Robot():
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port)
        self.send("import pyb")
        self.send("yaw_servo = pyb.Servo(1)")
        self.send("bottom_pitch_servo = pyb.Servo(2)")
        self.send("middle_pitch_servo = pyb.Servo(3)")
        self.send("top_pitch_servo = pyb.Servo(4)")
        self.servos = []
        self.yaw_servo = Servo(1)
        self.bottom_pitch_servo = Servo(2)
        self.middle_pitch_servo = Servo(3)
        self.top_pitch_servo = Servo(4)
        self.center()

    def send(self, comm):
        self.serial.write((comm + '\r\t\n').encode())

    def left(self):
        # self.send('yaw_servo.angle()')
        self.yaw_servo.angle -= move_amount
        if self.yaw_servo.angle < -90:
            self.yaw_servo.angle = -90

    def right(self):
        self.yaw_servo.angle += move_amount
        if self.yaw_servo.angle > 90:
            self.yaw_servo.angle = 90

    def up(self):
        self.bottom_pitch_servo.angle += move_amount
        if self.bottom_pitch_servo.angle > 90:
            self.bottom_pitch_servo.angle = 90

    def down(self):
        self.bottom_pitch_servo.angle -= move_amount
        if self.bottom_pitch_servo.angle < -90:
            self.bottom_pitch_servo.angle = -90

    def middle_up(self):
        self.middle_pitch_servo.angle += move_amount
        if self.middle_pitch_servo.angle > 90:
            self.middle_pitch_servo.angle = 90

    def middle_down(self):
        self.middle_pitch_servo.angle -= move_amount
        if self.middle_pitch_servo.angle < -90:
            self.middle_pitch_servo.angle = -90

    def top_up(self):
        self.top_pitch_servo.angle += move_amount
        if self.top_pitch_servo.angle > 90:
            self.top_pitch_servo.angle = 90

    def top_down(self):
        self.top_pitch_servo.angle -= move_amount
        if self.top_pitch_servo.angle < -90:
            self.top_pitch_servo.angle = -90

    def center(self):
        self.yaw_servo.angle = 0
        self.bottom_pitch_servo.set_angle(0)
        self.middle_pitch_servo.set_angle(0)
        self.top_pitch_servo.set_angle(0)

    def test_led(self):
        self.send('LED1.toggle()')

    def update(self, screen):
        self.send('yaw_servo.angle(' + str(self.yaw_servo.angle) + ')')
        self.send('yaw_servo.angle(' + str(self.bottom_pitch_servo.angle) + ')')
        self.send('yaw_servo.angle(' + str(self.middle_pitch_servo.angle) + ')')
        self.send('yaw_servo.angle(' + str(self.top_pitch_servo.angle) + ')')
        screen.fill((255, 255, 255))
        # TODO: Fix ground boundaries
        yaw_line_end = (YAW_INDICATOR_CENTER[0] + 100 * math.cos(math.radians(self.yaw_servo.angle - 90)),
                        YAW_INDICATOR_CENTER[1] + 100 * math.sin(math.radians(self.yaw_servo.angle - 90)))
        pygame.draw.line(screen, (0, 0, 0), yaw_line_end, YAW_INDICATOR_CENTER)
        bp_line_end = (PITCH_INDICATOR_CENTER[0] + 50 * math.cos(math.radians(self.bottom_pitch_servo.angle - 90)),
                       PITCH_INDICATOR_CENTER[1] + 50 * math.sin(math.radians(self.bottom_pitch_servo.angle - 90)))
        mp_line_end = (bp_line_end[0] + 40 * math.cos(
            math.radians(self.middle_pitch_servo.angle - 90 + self.bottom_pitch_servo.angle)),
                       bp_line_end[1] + 40 * math.sin(
                           math.radians(self.middle_pitch_servo.angle - 90 + self.bottom_pitch_servo.angle)))
        tp_line_end = (mp_line_end[0] + 30 * math.cos(
            math.radians(
                self.top_pitch_servo.angle - 90 + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle)),
                       mp_line_end[1] + 30 * math.sin(math.radians(
                           self.top_pitch_servo.angle - 90 + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle)))
        if mp_line_end[1] > PITCH_INDICATOR_CENTER[1]:
            mp_line_end = (mp_line_end[0], PITCH_INDICATOR_CENTER[1])
        if tp_line_end[1] > PITCH_INDICATOR_CENTER[1]:
            tp_line_end = (tp_line_end[0], PITCH_INDICATOR_CENTER[1])
        pygame.draw.line(screen, (0, 0, 0), (PITCH_INDICATOR_CENTER[0] - 50, PITCH_INDICATOR_CENTER[1]),
                         (PITCH_INDICATOR_CENTER[0] + 50, PITCH_INDICATOR_CENTER[1]), 2)
        pygame.draw.line(screen, (0, 0, 0), bp_line_end, PITCH_INDICATOR_CENTER)
        pygame.draw.line(screen, (0, 0, 0), mp_line_end, bp_line_end)
        pygame.draw.line(screen, (0, 0, 0), tp_line_end, mp_line_end)


robot = Robot('COM3')
command = {
    pygame.K_LEFT: robot.left,
    pygame.K_RIGHT: robot.right,
    pygame.K_UP: robot.up,
    pygame.K_DOWN: robot.down,
    pygame.K_w: robot.middle_up,
    pygame.K_s: robot.middle_down,
    pygame.K_e: robot.top_up,
    pygame.K_d: robot.top_down,
    pygame.K_SPACE: robot.center
}
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))
pygame.display.flip()
done = False
print('Ready for input')
while not done:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            done = True
        elif event == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    pressed = pygame.key.get_pressed()
    for key in command:
        if pressed[key]:
            command[key]()
    pygame.display.flip()
    robot.update(screen)
pygame.quit()