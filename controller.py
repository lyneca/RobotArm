import math

import serial
import pygame


move_amount = 0.5
__author__ = 'wing2048'
YAW_INDICATOR_CENTER = (360, 50)
PITCH_INDICATOR_CENTER = (130, 150)
FRICTION_CONSTANT = 0.8
TOUCH_ACCURACY = 20
TOP_ARM_LENGTH = 30
MIDDLE_ARM_LENGTH = 40
BOTTOM_ARM_LENGTH = 50
LIGHT_ANGLE = 10


class Servo():
    def __init__(self, servo_id):
        self.id = servo_id
        self.angle = 0
        self.velocity = 0

    def set_angle(self, angle):
        self.angle = angle


class Tool():
    def __init__(self):
        self.is_on = False

    def toggle(self):
        self.is_on = not self.is_on

    def on(self):
        self.is_on = True

    def off(self):
        self.is_on = False


class Robot():
    def __init__(self, port, tool_pin):
        self.port = port
        self.serial = serial.Serial(port)
        self.send("import pyb")
        self.send("tool_pin = pyb.Pin(" + tool_pin + ")")
        self.send('tool_led = pyb.LED(2)')
        self.send("yaw_servo = pyb.Servo(1)")
        self.send("bottom_pitch_servo = pyb.Servo(2)")
        self.send("middle_pitch_servo = pyb.Servo(3)")
        self.send("top_pitch_servo = pyb.Servo(4)")
        self.servos = []
        self.yaw_servo = Servo(1)
        self.bottom_pitch_servo = Servo(2)
        self.middle_pitch_servo = Servo(3)
        self.top_pitch_servo = Servo(4)
        self.tool_servo = Servo(5)
        self.tool = Tool()
        self.center()
        self.joints = []

    def send(self, comm):
        self.serial.write((comm + '\r\t\n').encode())

    def left(self, amount=move_amount):
        # self.send('yaw_servo.angle()')
        self.yaw_servo.angle -= amount
        if self.yaw_servo.angle < -90:
            self.yaw_servo.angle = -90

    def right(self, amount=move_amount):
        self.yaw_servo.angle += amount
        if self.yaw_servo.angle > 90:
            self.yaw_servo.angle = 90

    def up(self, amount=move_amount):
        self.bottom_pitch_servo.angle += amount
        if self.bottom_pitch_servo.angle > 90:
            self.bottom_pitch_servo.angle = 90

    def down(self, amount=move_amount):
        self.bottom_pitch_servo.angle -= amount
        if self.bottom_pitch_servo.angle < -90:
            self.bottom_pitch_servo.angle = -90

    def middle_up(self, amount=move_amount):
        self.middle_pitch_servo.angle += amount
        if self.middle_pitch_servo.angle > 90:
            self.middle_pitch_servo.angle = 90

    def middle_down(self, amount=move_amount):
        self.middle_pitch_servo.angle -= amount
        if self.middle_pitch_servo.angle < -90:
            self.middle_pitch_servo.angle = -90

    def top_up(self, amount=move_amount):
        self.top_pitch_servo.angle += amount
        if self.top_pitch_servo.angle > 90:
            self.top_pitch_servo.angle = 90

    def top_down(self, amount=move_amount):
        self.top_pitch_servo.angle -= amount
        if self.top_pitch_servo.angle < -90:
            self.top_pitch_servo.angle = -90

    def tool_up(self, amount=move_amount):
        self.tool_servo.angle += amount
        if self.tool_servo.angle < -90:
            self.tool_servo.angle = -90

    def tool_down(self, amount=move_amount):
        self.tool_servo.angle -= amount
        if self.tool_servo.angle < -90:
            self.tool_servo.angle = -90

    def center(self):
        self.yaw_servo.angle = 0
        self.yaw_servo.set_angle(0)
        self.bottom_pitch_servo.set_angle(0)
        self.middle_pitch_servo.set_angle(0)
        self.top_pitch_servo.set_angle(0)
        self.tool_servo.set_angle(0)

    def test_led(self):
        self.send('LED1.toggle()')

    # noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
    def update(self, screen):
        # OLD VELOCITY STUFF
        # self.yaw_servo.velocity *= FRICTION_CONSTANT
        # self.yaw_servo.angle += self.yaw_servo.velocity
        # self.top_pitch_servo.velocity *= FRICTION_CONSTANT
        # self.top_pitch_servo.angle += self.top_pitch_servo.velocity
        # self.middle_pitch_servo.velocity *= FRICTION_CONSTANT
        # self.middle_pitch_servo.angle += self.middle_pitch_servo.velocity
        # self.bottom_pitch_servo.velocity *= FRICTION_CONSTANT
        # self.bottom_pitch_servo.angle += self.bottom_pitch_servo.velocity
        if self.tool.is_on:
            self.send('tool_pin.high()')
            self.send('tool_led.on()')
        else:
            self.send('tool_pin.low()')
            self.send('tool_led.off()')
        self.send('yaw_servo.angle(' + str(self.yaw_servo.angle) + ')')
        self.send('yaw_servo.angle(' + str(self.bottom_pitch_servo.angle) + ')')
        self.send('yaw_servo.angle(' + str(self.middle_pitch_servo.angle) + ')')
        self.send('yaw_servo.angle(' + str(self.top_pitch_servo.angle) + ')')
        screen.fill((255, 255, 255))
        # TODO: Fix ground boundaries
        yaw_line_end = (
            round(YAW_INDICATOR_CENTER[0] + 100 * math.cos(math.radians(
                -1*(self.yaw_servo.angle + 90)))),
            round(YAW_INDICATOR_CENTER[1] + 100 * math.sin(math.radians(
                -1*(self.yaw_servo.angle + 90)))))
        yaw_line_end = (yaw_line_end[0], YAW_INDICATOR_CENTER[1] * 2 - yaw_line_end[1])
        bp_line_end = (
            round(PITCH_INDICATOR_CENTER[0] + BOTTOM_ARM_LENGTH * math.cos(math.radians(
                self.bottom_pitch_servo.angle - 90))),
            round(PITCH_INDICATOR_CENTER[1] + BOTTOM_ARM_LENGTH * math.sin(math.radians(
                self.bottom_pitch_servo.angle - 90))))
        mp_line_end = (
            round(bp_line_end[0] + MIDDLE_ARM_LENGTH * math.cos(math.radians(
                self.middle_pitch_servo.angle - 90 + self.bottom_pitch_servo.angle))),
            round(bp_line_end[1] + MIDDLE_ARM_LENGTH * math.sin(math.radians(
                self.middle_pitch_servo.angle - 90 + self.bottom_pitch_servo.angle))))
        tp_line_end = (
            round(mp_line_end[0] + TOP_ARM_LENGTH * math.cos(math.radians(
                self.top_pitch_servo.angle - 90 + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle))),
            round(mp_line_end[1] + TOP_ARM_LENGTH * math.sin(math.radians(
                self.top_pitch_servo.angle - 90 + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle))))
        if mp_line_end[1] > PITCH_INDICATOR_CENTER[1]:
            mp_line_end = (mp_line_end[0], PITCH_INDICATOR_CENTER[1])
        if tp_line_end[1] > PITCH_INDICATOR_CENTER[1]:
            tp_line_end = (tp_line_end[0], PITCH_INDICATOR_CENTER[1])
        compass = pygame.image.load('protractor.jpg')
        pygame.draw.rect(screen, (0, 0, 0), (screen.get_rect().width / 2 - 50, 200, 100, 50), 5)
        pygame.draw.circle(screen, (0, 0, 0), PITCH_INDICATOR_CENTER, 3)
        pygame.draw.circle(screen, (0, 0, 0), bp_line_end, 3)
        pygame.draw.circle(screen, (0, 0, 0), mp_line_end, 3)
        compensation = self.top_pitch_servo.angle + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle + self.tool_servo.angle - 90
        if self.tool.is_on:
            pygame.draw.polygon(screen, (255, 255, 0), (tp_line_end,
                                                        (tp_line_end[0]+30*math.cos(math.radians(LIGHT_ANGLE+compensation)), tp_line_end[1]+30*math.sin(math.radians(LIGHT_ANGLE+compensation))),
                                                        (tp_line_end[0]+30*math.cos(math.radians(-LIGHT_ANGLE+compensation)), tp_line_end[1]+30*math.sin(math.radians(-LIGHT_ANGLE+compensation)))))
            pygame.draw.rect(screen, (0, 255, 0), (screen.get_rect().width / 2 - 45, 205, 90, 40))
            pygame.draw.rect(screen, (0, 0, 0),
                             (tp_line_end[0] - 2, tp_line_end[1] - 2, 5, 5))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (screen.get_rect().width / 2 - 45, 205, 90, 40))
            pygame.draw.circle(screen, (0, 0, 0), tp_line_end, 3)
        tool_text = font.render('TOOL', 25, (0, 0, 0))
        pitch_text = font.render('ARM PITCH', 25, (0, 0, 0))
        yaw_text = font.render('YAW', 25, (0, 0, 0))
        screen.blit(pygame.transform.smoothscale(compass, (201, 110)),
                    (YAW_INDICATOR_CENTER[0] - 100, YAW_INDICATOR_CENTER[1] - 5))
        pygame.draw.circle(screen, (0, 0, 0), yaw_line_end, 3)
        screen.blit(tool_text, (screen.get_rect().centerx - tool_text.get_rect().width / 2, 170))
        screen.blit(pitch_text,
                    (PITCH_INDICATOR_CENTER[0] - pitch_text.get_rect().width / 2, PITCH_INDICATOR_CENTER[1] + 10))
        screen.blit(yaw_text, (YAW_INDICATOR_CENTER[0] - yaw_text.get_rect().width / 2, YAW_INDICATOR_CENTER[1] + 110))
        pygame.draw.aaline(screen, (0, 0, 0), yaw_line_end, YAW_INDICATOR_CENTER)
        pygame.draw.aaline(screen, (0, 0, 0), (PITCH_INDICATOR_CENTER[0] - 50, PITCH_INDICATOR_CENTER[1]),
                           (PITCH_INDICATOR_CENTER[0] + 50, PITCH_INDICATOR_CENTER[1]), 2)
        pygame.draw.aaline(screen, (0, 0, 0), bp_line_end, PITCH_INDICATOR_CENTER)
        pygame.draw.aaline(screen, (0, 0, 0), mp_line_end, bp_line_end)
        pygame.draw.aaline(screen, (0, 0, 0), tp_line_end, mp_line_end, 4)
        self.bottom_joint = pygame.Rect(
            bp_line_end[0] - TOUCH_ACCURACY, bp_line_end[1] - TOUCH_ACCURACY, TOUCH_ACCURACY * 2, TOUCH_ACCURACY * 2)
        self.middle_joint = pygame.Rect(
            mp_line_end[0] - TOUCH_ACCURACY, mp_line_end[1] - TOUCH_ACCURACY, TOUCH_ACCURACY * 2, TOUCH_ACCURACY * 2)
        self.top_joint = pygame.Rect(
            tp_line_end[0] - TOUCH_ACCURACY, tp_line_end[1] - TOUCH_ACCURACY, TOUCH_ACCURACY * 2, TOUCH_ACCURACY * 2)
        self.yaw_joint = pygame.Rect(
            yaw_line_end[0] - TOUCH_ACCURACY, yaw_line_end[1] - TOUCH_ACCURACY, TOUCH_ACCURACY * 2, TOUCH_ACCURACY * 2)
        self.joints = {
            'bottom': self.bottom_joint,
            'middle': self.middle_joint,
            'top': self.top_joint,
            'yaw': self.yaw_joint
        }


robot = Robot('COM3', 'Y1')
command = {
    pygame.K_LEFT: robot.left,
    pygame.K_RIGHT: robot.right,
    pygame.K_UP: robot.up,
    pygame.K_DOWN: robot.down,
    pygame.K_q: robot.middle_up,
    pygame.K_a: robot.middle_down,
    pygame.K_w: robot.top_up,
    pygame.K_s: robot.top_down,
    pygame.K_c: robot.center,
    pygame.K_e: robot.tool_up,
    pygame.K_d: robot.tool_down
}
pygame.init()
font = pygame.font.SysFont('Courier', 25)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 300), pygame.FULLSCREEN)
screen.fill((255, 255, 255))
pygame.display.flip()
done = False
robot.update(screen)
print('Ready for input')
while not done:
    moving = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            active_joint = False
            for key in robot.joints:
                joint = robot.joints[key]
                if joint.collidepoint(mouse_pos):
                    active_joint = key
                    moving = True
            mouse_pos = pygame.mouse.get_pos()
            sx = screen.get_rect().width / 2 - 45
            sy = 205
            bx = sx + 90
            by = sy + 40
            if sx <= mouse_pos[0] <= bx:
                if sy <= mouse_pos[1] <= by:
                    robot.tool.toggle()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_SPACE:
                robot.tool.toggle()
    if moving:
        while pygame.mouse.get_pressed()[0]:
            joint_lib = {
                'top': robot.middle_joint.center,
                'middle': robot.bottom_joint.center,
                'bottom': PITCH_INDICATOR_CENTER,
                'yaw': YAW_INDICATOR_CENTER
            }
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]
            pygame.event.clear()
            connecting_joint = joint_lib[active_joint]
            if active_joint == 'yaw':
                angle = (math.degrees(math.atan2(connecting_joint[1] - mouse_y, connecting_joint[0] - mouse_x)) + 90)
            else:
                angle = (math.degrees(math.atan2(connecting_joint[1] - mouse_y, connecting_joint[0] - mouse_x)) - 90)
            if -180 > angle:
                n_angle = angle % 360
            else:
                n_angle = angle
            if active_joint == 'top':
                if -90 + robot.bottom_pitch_servo.angle + robot.middle_pitch_servo.angle <= n_angle <= 90 + robot.bottom_pitch_servo.angle + robot.middle_pitch_servo.angle:
                    robot.top_pitch_servo.set_angle(n_angle - robot.middle_pitch_servo.angle - robot.bottom_pitch_servo.angle)
            elif active_joint == 'middle':
                if -90 + robot.bottom_pitch_servo.angle <= n_angle <= 90 + robot.bottom_pitch_servo.angle:
                    robot.middle_pitch_servo.set_angle(n_angle - robot.bottom_pitch_servo.angle)
            elif active_joint == 'bottom':
                if -90 <= angle <= 90:
                    robot.bottom_pitch_servo.set_angle(n_angle)
            else:
                if -90 <= angle <= 90:
                    robot.yaw_servo.set_angle(n_angle)
            robot.update(screen)
            pygame.display.flip()
        moving = False
    pressed = pygame.key.get_pressed()
    for key in command:
        if pressed[key]:
            command[key]()
    pygame.display.flip()
    robot.update(screen)
screen = pygame.display.set_mode((500, 300))
pygame.quit()