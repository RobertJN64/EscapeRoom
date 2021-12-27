import pygame
import math
import time
import datetime
pygame.init()

print()

with open('pin.txt') as f:
    correctpin = f.read().strip()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(screen, text, pos, color=(255,0,0), size=30):
    largeText = pygame.font.SysFont("Consolas", size)
    TextSurf, TextRect = text_objects(str(text), largeText, color)
    TextRect.center = pos
    screen.blit(TextSurf, TextRect)

def parseTimer(t):
    if len(t) == 4:
        return int(t[0]) * 60 + int(t[2:4])
    else:
        return int(t[0:2]) * 60 + int(t[3:5])

def leadingZero(num: int):
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)

def parseSeconds(t):
    return leadingZero(math.floor(t/60)) + ':' + leadingZero(t%60)

timer = '45:00'
seconds = parseTimer(timer)

def main():
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    isfull = False

    done = False
    pin = "* * * *"
    pinpos = 0
    running = False

    lval = time.time()
    end = time.time() + seconds

    img = pygame.image.load('mars.jpg')
    img2 = pygame.image.load('gear.png')
    img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
    img2 = pygame.transform.scale(img2, (img2.get_width() * 0.1, img2.get_height() * 0.1))

    drawpos = 0

    c = pygame.time.Clock()
    count = 0
    delta = -1

    update = True

    while not done:
        screen.fill((100, 100, 100))

        if update:
            screen.blit(img, (drawpos,-40))
            screen.blit(img2, (drawpos + 1750, 500))

        if count > 3:
            drawpos += delta
            count = 0
        count += 1

        if (img.get_width() + drawpos) < (screen.get_width() + 10):
            delta = 1

        if drawpos == 0:
            delta = -1

        centerx = screen.get_width() / 2
        centery = screen.get_height() / 2 - 100

        pygame.draw.rect(screen, (0, 0, 0), (centerx - 100, centery - 35, 200, 150))

        if not running:
            end = time.time() + seconds
            pintext = "WAIT FOR START"
            lval = time.time()
        elif time.time() > end:
            pintext = "OVERTIME"
            lval = end
        elif pin == correctpin:
            pintext = "CORRECT"
        elif '*' in pin:
            pintext = "ENTER PIN"
            lval = time.time()
        else:
            pintext = "INCORRECT"
            lval = time.time()

        message_display(screen, 'Camera_4', (60,30), color=(255,255,255), size=20)
        message_display(screen, datetime.datetime.now().strftime('%B %d %#I:%M:%S %p'), (100, 50),
                        color=(255, 255, 255), size=15)
        message_display(screen, parseSeconds(round(end - lval)), (centerx, centery), size=50)
        message_display(screen, pin, (centerx, centery + 60))
        message_display(screen, pintext, (centerx, centery+100), size=20)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'backspace':
                    pin = "* * * *"
                    pinpos = 0
                elif key == "p": #penalty:
                    end -= 60 * 10
                elif key == "u": #update:
                    update = not update
                elif key == "s": #start
                    running = True
                elif key == "f":
                    if not isfull:
                        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                    isfull = not isfull
                else:
                    try:
                        if pinpos == 8:
                            pass
                        else:
                            int(key)
                            pin = list(pin)
                            pin[pinpos] = key
                            pin = "".join(pin)
                            pinpos += 2

                    except ValueError:
                        pass

        c.tick(100)

main()