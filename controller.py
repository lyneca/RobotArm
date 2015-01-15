import serial
import pygame

__author__ = 'wing2048'


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
        self.yaw_servo = 0
        self.bottom_pitch_servo = 0
        self.middle_pitch_servo = 0
        self.top_pitch_servo = 0
        self.servos.append(self.yaw_servo)
        self.servos.append(self.bottom_pitch_servo)
        self.servos.append(self.middle_pitch_servo)
        self.servos.append(self.top_pitch_servo)
        self.center()
    def send(self, comm):
        self.serial.write((comm + '\r\t\n').encode())

    # TODO udlr functions
    def left(self):
        self.send()

    def right(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def center(self):
        self.yaw_servo = 0
        self.bottom_pitch_servo = 0
        self.middle_pitch_servo = 0
        self.top_pitch_servo = 0

    def test_led(self):
        self.send('LED1.toggle()')

    def update(self):
        self.send('yaw_servo.angle(' + str(self.yaw_servo) + ')')
        self.send('yaw_servo.angle(' + str(self.bottom_pitch_servo) + ')')
        self.send('yaw_servo.angle(' + str(self.middle_pitch_servo) + ')')
        self.send('yaw_servo.angle(' + str(self.top_pitch_servo) + ')')

robot = Robot('COM3')
command = {
    pygame.K_LEFT: robot.left,
    pygame.K_RIGHT: robot.right,
    pygame.K_UP: robot.up,
    pygame.K_DOWN: robot.down,
    pygame.K_SPACE: robot.test_led
}
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((100, 100))
screen.fill((0, 0, 0))
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
    clock.tick(60)
pygame.quit()