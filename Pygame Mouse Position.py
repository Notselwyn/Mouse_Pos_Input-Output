import pygame
import datetime
import sys


def main():
    pygame.init()
    clock = pygame.time.Clock()
    size = [256, 356]

    # transparent = (0, 0, 0, 0)
    white = [255, 255, 255]
    black = [0, 0, 0]

    pygame.display.set_caption('Get Mouse Pos')
    IconImg = pygame.image.load(r'C:\Users\Wit\Desktop\Programming shit\img\icon.png')
    pygame.display.set_icon(IconImg)

    screen = pygame.display.set_mode(size)

    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Replay tracers', True, black, white)
    textRect = text.get_rect()
    textRect.center = (128, 276)

    button = pygame.Rect(103, 296, 50, 50)  # creates a rect object

    screen.fill(white)
    GridImg = pygame.image.load(r'C:\Users\Wit\Desktop\Programming shit\img\grid.png')
    GridImg = pygame.transform.scale(GridImg, (256, 256))
    screen.blit(GridImg, (0, 0))
    GridImg.set_alpha(15)

    greenPx = pygame.image.load(r'C:\Users\Wit\Desktop\Programming shit\img\greenPx.png')
    redPx = pygame.image.load(r'C:\Users\Wit\Desktop\Programming shit\img\redpx.png')

    screen.blit(text, textRect)
    pygame.draw.rect(screen, [255, 0, 0], button)  # draw button

    MousePosList = []
    tracerNum = 0
    running = True
    down = False
    datetime_delay = datetime.datetime.now()

    while running is True:
        screen.blit(GridImg, (0, 0))
        mousepos = pygame.mouse.get_pos()
        datetime_now = datetime.datetime.now()
        down_cap = float((datetime_now - datetime_delay).total_seconds())

        if down:
            screen.blit(redPx, MousePosList[tracerNum])
            sys.stdout.write(f"\r{MousePosList[tracerNum]}")
            tracerNum += 1
            if tracerNum == len(MousePosList):
                tracerNum = 0

        if down and down_cap <= .4:
            pygame.draw.rect(screen, [200, 0, 0], button)
        elif not down and down_cap >= .4:
            pygame.draw.rect(screen, [255, 0, 0], button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    running = False
                    return running
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(mousepos) and down_cap >= .4:
                    for x, y in enumerate(MousePosList):
                        screen.blit(greenPx, y)
                    datetime_delay = datetime.datetime.now()
                    tracerNum = 0
                    down = True
            elif event.type == pygame.MOUSEBUTTONUP and down:
                down = False

        if 0 <= mousepos[1] <= 255 and 0 <= mousepos[0] <= 255 and MousePosList.count(mousepos) < 3 and not down:
            screen.blit(greenPx, mousepos)
            MousePosList.append(mousepos)
            sys.stdout.write(f"\r{mousepos}")
            sys.stdout.flush()

        pygame.display.flip()
        clock.tick(144)
    pygame.quit()
    sys.exit


if __name__ == '__main__':
    main()
