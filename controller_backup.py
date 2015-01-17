import math
import serial
import pygame
import time

move_amount = 0.5
__author__ = 'wing2048'
YAW_INDICATOR_CENTER = (360, 50)
PITCH_INDICATOR_CENTER = (130, 150)
FRICTION_CONSTANT = 0.8

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
        self.tool = Tool()
        self.center()

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

    def center(self):
        self.yaw_servo.angle = 0
        self.yaw_servo.set_angle(0)
        self.bottom_pitch_servo.set_angle(0)
        self.middle_pitch_servo.set_angle(0)
        self.top_pitch_servo.set_angle(0)

    def test_led(self):
        self.send('LED1.toggle()')

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
        yaw_line_end = (YAW_INDICATOR_CENTER[0] + 100 * math.cos(math.radians(self.yaw_servo.angle - 90)),
                        YAW_INDICATOR_CENTER[1] + 100 * math.sin(math.radians(self.yaw_servo.angle - 90)))
        yaw_line_end = (yaw_line_end[0], YAW_INDICATOR_CENTER[1] * 2 - yaw_line_end[1])
        bp_line_end = (
        round(PITCH_INDICATOR_CENTER[0] + 50 * math.cos(math.radians(self.bottom_pitch_servo.angle - 90))),
        round(PITCH_INDICATOR_CENTER[1] + 50 * math.sin(math.radians(self.bottom_pitch_servo.angle - 90))))
        mp_line_end = (round(bp_line_end[0] + 40 * math.cos(
            math.radians(self.middle_pitch_servo.angle - 90 + self.bottom_pitch_servo.angle))),
                       round(bp_line_end[1] + 40 * math.sin(
                           math.radians(self.middle_pitch_servo.angle - 90 + self.bottom_pitch_servo.angle))))
        tp_line_end = (round(mp_line_end[0] + 30 * math.cos(
            math.radians(
                self.top_pitch_servo.angle - 90 + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle))),
                       round(mp_line_end[1] + 30 * math.sin(math.radians(
                           self.top_pitch_servo.angle - 90 + self.middle_pitch_servo.angle + self.bottom_pitch_servo.angle))))
        if mp_line_end[1] > PITCH_INDICATOR_CENTER[1]:
            mp_line_end = (mp_line_end[0], PITCH_INDICATOR_CENTER[1])
        if tp_line_end[1] > PITCH_INDICATOR_CENTER[1]:
            tp_line_end = (tp_line_end[0], PITCH_INDICATOR_CENTER[1])
        compass = pygame.image.load('protractor.jpg')
        pygame.draw.rect(screen, (0, 0, 0), (screen.get_rect().width/2-50, 200, 100, 50), 5)
        pygame.draw.circle(screen, (0, 0, 0), PITCH_INDICATOR_CENTER, 3)
        pygame.draw.circle(screen, (0, 0, 0), bp_line_end, 3)
        pygame.draw.circle(screen, (0, 0, 0), mp_line_end, 3)
        if self.tool.is_on:
            pygame.draw.rect(screen, (0, 255, 0), (screen.get_rect().width/2-45, 205, 90, 40))
            pygame.draw.circle(screen, (0, 0, 0), tp_line_end, 3)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (screen.get_rect().width/2-45, 205, 90, 40))
            pygame.draw.rect(screen, (0, 0, 0),
                             (tp_line_end[0]-2, tp_line_end[1]-2, 5, 5))
        tool_text = font.render('TOOL', 25, (0, 0, 0))
        pitch_text = font.render('ARM PITCH', 25, (0, 0, 0))
        yaw_text = font.render('YAW', 25, (0, 0, 0))
        screen.blit(pygame.transform.smoothscale(compass, (201, 110)),
                    (YAW_INDICATOR_CENTER[0] - 100, YAW_INDICATOR_CENTER[1] - 5))
        screen.blit(tool_text, (screen.get_rect().centerx-tool_text.get_rect().width/2, 170))
        screen.blit(pitch_text, (PITCH_INDICATOR_CENTER[0]-pitch_text.get_rect().width / 2, PITCH_INDICATOR_CENTER[1] + 10))
        screen.blit(yaw_text, (YAW_INDICATOR_CENTER[0]-yaw_text.get_rect().width / 2, YAW_INDICATOR_CENTER[1] + 110))
        pygame.draw.aaline(screen, (0, 0, 0), yaw_line_end, YAW_INDICATOR_CENTER)
        pygame.draw.aaline(screen, (0, 0, 0), (PITCH_INDICATOR_CENTER[0] - 50, PITCH_INDICATOR_CENTER[1]),
                           (PITCH_INDICATOR_CENTER[0] + 50, PITCH_INDICATOR_CENTER[1]), 2)
        pygame.draw.aaline(screen, (0, 0, 0), bp_line_end, PITCH_INDICATOR_CENTER)
        pygame.draw.aaline(screen, (0, 0, 0), mp_line_end, bp_line_end)
        pygame.draw.aaline(screen, (0, 0, 0), tp_line_end, mp_line_end, 4)


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
}
pygame.init()
font = pygame.font.SysFont('Courier', 25)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 300))
screen.fill((255, 255, 255))
pygame.display.flip()
done = False
print('Ready for input')
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            sx = screen.get_rect().width/2-45
            sy = 205
            bx = sx + 90
            by = sy + 40
            if mouse_pos[0] >= sx and mouse_pos[0] <= bx:
                if mouse_pos[1] >= sy and mouse_pos[1] <= by:
                    robot.tool.toggle()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_SPACE:
                print(robot.tool.is_on)
                robot.tool.toggle()
    pressed = pygame.key.get_pressed()
    for key in command:
        if pressed[key]:
            command[key]()
    pygame.display.flip()
    robot.update(screen)
pygame.quit()