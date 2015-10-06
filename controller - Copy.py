__author__ = 'wing2048'
from classes import *
from constants import *

print('Constants set.')

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
screen = pygame.display.set_mode((500, 300))
screen.fill((255, 255, 255))
pygame.display.flip()
done = False
robot.update(screen)
print('Screen ready.')
print('Ready for input.')
command_string = ''
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
            sx = screen.get_rect().width / 2 + 105
            sy = 205
            bx = sx + 90
            by = sy + 40
            if sx <= mouse_pos[0] <= bx:
                if sy <= mouse_pos[1] <= by:
                    robot.center()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                print('Enter gesture name:')
                gesture = input(': ')
                if gesture in robot.gestures:
                    robot.gesture_interpret(robot.gestures[gesture], screen)
            if event.key == pygame.K_v:
                print('Yaw:    ', robot.yaw_servo.angle)
                print('Bottom: ', robot.bottom_pitch_servo.angle)
                print('Middle: ', robot.middle_pitch_servo.angle)
                print('Top:    ', robot.top_pitch_servo.angle)
            if event.key == pygame.K_RETURN:
                print('Enter command sequence string:')
                command_string = input(': ')
                robot.interpret(command_string, screen)
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
                if -75 + robot.bottom_pitch_servo.angle + robot.middle_pitch_servo.angle <= n_angle <= 64 + \
                        robot.bottom_pitch_servo.angle + robot.middle_pitch_servo.angle:
                    robot.top_pitch_servo.set_angle(
                        n_angle - robot.middle_pitch_servo.angle - robot.bottom_pitch_servo.angle)
            elif active_joint == 'middle':
                if -75 + robot.bottom_pitch_servo.angle <= n_angle <= 64 + robot.bottom_pitch_servo.angle:
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
    true_top_angle = robot.top_pitch_servo.angle + robot.middle_pitch_servo.angle + robot.bottom_pitch_servo.angle
    true_middle_angle = robot.middle_pitch_servo.angle + robot.bottom_pitch_servo.angle
    if robot.top_pitch_servo.angle + 0.5 < -70:
        robot.top_pitch_servo.set_angle(-70)
    elif robot.top_pitch_servo.angle > 60:
        robot.top_pitch_servo.set_angle(60)
    if robot.middle_pitch_servo.angle < -70:
        robot.middle_pitch_servo.set_angle(-70)
    elif robot.middle_pitch_servo.angle > 60:
        robot.middle_pitch_servo.set_angle(60)
    robot.update(screen)
    pygame.display.flip()
    if done:
        robot.force_center()
    # while True:
    #     eval(input('>>> '))
pygame.display.flip()
print('Exiting...')
screen = pygame.display.set_mode((500, 300))
pygame.quit()