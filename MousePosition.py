import pygame
import datetime
import sys
import os
import pathlib


def draw_window(tracers=True, replayTracers=False, flushTracers=False, size=256, flushChat=True, fps=160):
    """" Draw a window to extract coordinates from.
    
    :param tracers: Draw tracers.
    :type tracers: bool
    
    :param replayTracers: Ability to replay tracers.
    :type replayTracers: bool

    :param flushTracers: Flush replayed tracers.
    :type flushTracers: bool
    
    :param size: Size of the window.
    :type size: bool
    
    :param flushChat: Flush the coordinates in the chat. Slower but keeps it clean.
    :type flushChat: bool
    
    :param fps: Frames per second. Recommended is 100 to 300.
    :type fps: int
    
    """

    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Get Mouse Pos')
    print()
    IconImg = pygame.image.load(os.path.join(f"{pathlib.Path(__file__).parent.absolute()}/img", "icon.png"))
    pygame.display.set_icon(IconImg)
    
    # makes window larger for replay tracers button
    if replayTracers:
        size = [size, size+100]
    elif not replayTracers:
        size = [size, size]

    screen = pygame.display.set_mode(size)

    # declaring props
    button = pygame.Rect(103, 296, 50, 50)
    button.center = [size[0]/2, size[1]-40]

    screen.fill([255, 255, 255])
    GridImg = pygame.image.load(os.path.join(f"{pathlib.Path(__file__).parent.absolute()}/img", "grid.png"))
    GridImg = pygame.transform.scale(GridImg, (size[0], size[0]))
    screen.blit(GridImg, (0, 0))
    GridImg.set_alpha(15)
    
    # declares tracer info
    if tracers:
        greenPx = pygame.image.load(os.path.join(f"{pathlib.Path(__file__).parent.absolute()}/img", "greenpx.png"))
    
    if replayTracers:
        redPx = pygame.image.load(os.path.join(f"{pathlib.Path(__file__).parent.absolute()}/img", "redpx.png"))

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Replay tracers', True, [0, 0, 0], [255, 255, 255])
        textRect = text.get_rect()
        textRect.center = (size[0]/2, size[1]-80)

        screen.blit(text, textRect)
        pygame.draw.rect(screen, [255, 0, 0], button)

    # default values; delay can be tweaked.
    datetime_delay = datetime.datetime.now()
    MousePosList = []
    tracerNum = 0
    down = False
    delay = .1

    while True:
        # print stuff to the screen
        screen.blit(GridImg, (0, 0))
        mousepos = pygame.mouse.get_pos()
        datetime_now = datetime.datetime.now()
        down_cap = float((datetime_now - datetime_delay).total_seconds())

        if down and down_cap <= delay and replayTracers:
            pygame.draw.rect(screen, [200, 0, 0], button)
        elif not down and down_cap >= delay and replayTracers:
            pygame.draw.rect(screen, [255, 0, 0], button)

        # replay tracers
        if down and len(MousePosList) > 0:    
            screen.blit(redPx, MousePosList[tracerNum])
            sys.stdout.write(f"\r{MousePosList[tracerNum]}")
            tracerNum += 1
            if tracerNum == len(MousePosList):
                tracerNum = 0

        for event in pygame.event.get():
            # stop process
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    return False

            # draw tracers on mouse
            elif replayTracers is True and event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(mousepos) and down_cap >= delay:
                for y in MousePosList:
                    screen.blit(greenPx, y)
                datetime_delay = datetime.datetime.now()
                tracerNum = 0
                down = True

            # reset replay tracers list after button press
            elif event.type == pygame.MOUSEBUTTONUP and down:
                if flushTracers:
                    MousePosList = []
                down = False

        if 0 <= mousepos[1] <= size[0] and 0 <= mousepos[0] <= size[0] and MousePosList.count(mousepos) < 3 and not down:
            # add mouse pos to tracers list so it can be replayed later
            if tracers:
                screen.blit(greenPx, mousepos)
                MousePosList.append(mousepos)

            # flushes chat instead of spamming
            if flushChat:
                sys.stdout.flush()
                sys.stdout.write(f"\r{mousepos}")
            else:
                print(str(mousepos), end='\n')

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    sys.exit()
