import serial
import pygame

__author__ = 'wing2048'


class Robot():
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port)
        self.send("import pyb")
        # TODO Add pin numbers
        self.send("yaw_servo = pyb.pin()")
        self.send("bottom_pitch_servo = pyb.pin()")
        self.send("middle_pitch_servo = pyb.pin()")

    def send(self, comm):
        self.serial.write((comm + '\r\t\n').encode())

    def left(self):
        pass

    def right(self):
        pass

    def up(self):
        pass

    def down(self):
        pass


robot = Robot('COM3')
command = {
    pygame.K_LEFT: robot.left(),
    pygame.K_RIGHT: robot.right(),
    pygame.K_UP: robot.up(),
    pygame.K_DOWN: robot.down()
}
pygame.init()

while True:
    pressed = pygame.key.get_pressed()
    for key in pressed:
        command[key]