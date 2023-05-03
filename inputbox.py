import pygame as pg
width, height = 1276, 627
win = pg.display.set_mode((width, height))

def gameover(screen):
    highscore_background = pg.image.load("images/logo.png")
    # bg = pg.image.load("images/BG.png") #background

    font = pg.font.Font(None, 64)
    clock = pg.time.Clock()
    input_box = pg.Rect(600, 400, 600, 64)
    color_inactive = pg.Color('black')
    color_active = pg.Color('blue')
    color = color_inactive

    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        return text

                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((210, 210, 210))

        screen.blit(highscore_background, (263,131))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        screen.blit(font.render('Имя:', 1, color), (430, 410))
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    gameover(win)

    pg.quit()