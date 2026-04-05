import socket
import pygame
import time

HOST = "192.168.4.1"
PORT = 80

def send_command(cmd: str):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        s.connect((HOST, PORT))
        s.sendall((cmd + "\n").encode("utf-8"))
        s.close()
        print(f"Enviado: {cmd}")
    except Exception as e:
        print(f"Error enviando '{cmd}': {e}")

pygame.init()
screen = pygame.display.set_mode((640, 240))
pygame.display.set_caption("Control WiFi del carro")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()

# Estado actual
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False

last_motor_cmd = None
last_steer_cmd = None

def resolve_motor_command():
    if w_pressed and not s_pressed:
        return "w"
    if s_pressed and not w_pressed:
        return "s"
    return "x"

def resolve_steer_command():
    if a_pressed and not d_pressed:
        return "a"
    if d_pressed and not a_pressed:
        return "d"
    return "c"

running = True
send_command("x")
send_command("c")
time.sleep(0.1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                w_pressed = True
            elif event.key == pygame.K_s:
                s_pressed = True
            elif event.key == pygame.K_a:
                a_pressed = True
            elif event.key == pygame.K_d:
                d_pressed = True
            elif event.key == pygame.K_q:
                running = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                w_pressed = False
            elif event.key == pygame.K_s:
                s_pressed = False
            elif event.key == pygame.K_a:
                a_pressed = False
            elif event.key == pygame.K_d:
                d_pressed = False

    motor_cmd = resolve_motor_command()
    steer_cmd = resolve_steer_command()

    if motor_cmd != last_motor_cmd:
        send_command(motor_cmd)
        last_motor_cmd = motor_cmd

    if steer_cmd != last_steer_cmd:
        send_command(steer_cmd)
        last_steer_cmd = steer_cmd

    screen.fill((30, 30, 30))
    lines = [
        "Controles: W/S mover | A/D direccion | Q salir",
        f"W={w_pressed} S={s_pressed} A={a_pressed} D={d_pressed}",
        f"Motor: {motor_cmd}",
        f"Direccion: {steer_cmd}",
    ]

    y = 40
    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (30, y))
        y += 40

    pygame.display.flip()
    clock.tick(60)

# Seguridad al salir
send_command("x")
send_command("c")
pygame.quit()