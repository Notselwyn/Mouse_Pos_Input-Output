import pygame
import datetime
import sys
import os


def main(tracers=True, replayTracers=False):
    pygame.init()
    clock = pygame.time.Clock()
    if replayTracers:
        size = [256, 356]
    elif not replayTracers:
        size = [256, 256]

    pygame.display.set_caption('Get Mouse Pos')
    IconImg = pygame.image.load(os.path.join("img", "icon.png"))
    pygame.display.set_icon(IconImg)

    screen = pygame.display.set_mode(size)

    button = pygame.Rect(103, 296, 50, 50)  # creates a rect object

    screen.fill([255, 255, 255])
    GridImg = pygame.image.load(os.path.join("img", "grid.png"))
    GridImg = pygame.transform.scale(GridImg, (256, 256))
    screen.blit(GridImg, (0, 0))
    GridImg.set_alpha(15)

    if tracers:
        greenPx = pygame.image.load(os.path.join("img", "greenpx.png"))
    if replayTracers:
        redPx = pygame.image.load(os.path.join("img", "redpx.png"))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Replay tracers', True, [0, 0, 0], [255, 255, 255])
        textRect = text.get_rect()
        textRect.center = (128, 276)

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

        if down and down_cap <= .4 and replayTracers:
            pygame.draw.rect(screen, [200, 0, 0], button)
        elif not down and down_cap >= .4 and replayTracers:
            pygame.draw.rect(screen, [255, 0, 0], button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    running = False
                    return running
            if replayTracers is True and event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(mousepos) and down_cap >= .4:
                for y in MousePosList:
                    screen.blit(greenPx, y)
                datetime_delay = datetime.datetime.now()
                tracerNum = 0
                down = True
            elif event.type == pygame.MOUSEBUTTONUP and down:
                down = False

        if 0 <= mousepos[1] <= 255 and 0 <= mousepos[0] <= 255 and MousePosList.count(mousepos) < 3 and not down:
            if tracers:
                screen.blit(greenPx, mousepos)
                MousePosList.append(mousepos)
            sys.stdout.write(f"\r{mousepos}")
            sys.stdout.flush()

        pygame.display.flip()
        clock.tick(150)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
    # Args:
    # replayTracers (Bool): Triggers being able to replay tracers
    # tracers (Bool): Triggers being able to see tracers
