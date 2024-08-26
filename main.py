import pygame as pg
import classes

# INICIADORES PADRÕES..............................................:
pg.init()
pg.font.init()
font_30 = pg.font.Font('ARCADECLASSIC.TTF', 100)

# TELA_____________________________________________________________:
larg = 1280
alt = 720
screen = pg.display.set_mode((larg, alt))
pg.display.set_caption('simetr_io')
clock = pg.time.Clock()
screen.fill((127, 205, 255))


# MAIN MENU_________________________________________________________:
def main_menu():
    menu_run = True
    all_buttons = pg.sprite.Group()
    mirrors = pg.sprite.Group()
    start_game = classes.Button(screen, 'Iniciar', larg/2, alt/2, 30)
    exit_game = classes.Button(screen, 'Sair', larg/2, alt/2 + 100, 30)
    name_game = classes.Button(screen, 'SIMETRIO', larg/2, alt/2 - 150, 100)
    mirror2 = classes.Mirror(875, alt/2 - 150, False)
    mirror1 = classes.Mirror(400, alt/2 - 150, True)
    all_buttons.add(start_game, exit_game)
    mirrors.add(mirror2, mirror1)

    # MAIN LOOP_____________________________________________________:
    while menu_run:
        clock.tick(30)
        click = False
        mx, my = pg.mouse.get_pos()

        # GET DE EVENTOS____________________________________________:
        for event in pg.event.get():
            # GAME QUIT_____________________________________________:
            if event.type == pg.QUIT:
                pg.quit()
                break

            # MOUSE CLICK___________________________________________:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

            # COLISAO DOS BOTOES____________________________________:
            if click:
                start_game.clicked(mx, my)
                exit_game.clicked(mx, my)

        # ACAO DOS BOTOES___________________________________________:
        if start_game.update():
            menu_run = False
            screen.fill((127, 205, 255))
            pick()

        elif exit_game.update():
            menu_run = False
            pg.quit()

        # RENDER / ATT DOS BOTOES___________________________________:
        all_buttons.draw(screen)
        mirrors.draw(screen)
        name_game.render_text()
        for button in all_buttons:
            button.render_text()

        # ATT DA TELA_______________________________________________:
        pg.display.update()
        pg.display.flip()


def pick():
    pick_run = True
    all_buttons = pg.sprite.Group()
    animals = pg.sprite.Group()

    fundo = classes.Fundo()
    bilaterio = classes.Bilaterio(alt, larg, screen)
    bilaterio.x, bilaterio.y = larg/4 + 150, alt/2 - 50
    title = classes.Button(screen, 'ESCOLHA  UM  ANIMAL', larg/2, 100, 60)
    radial = classes.Radial(alt, larg, screen)
    radial.x, radial.y = 3/4 * larg - 150, alt/2 - 50
    radial.rect.center = radial.x, radial.y
    bilaterio.rect.center = bilaterio.x, bilaterio.y

    pick_bilaterio = classes.Button(screen, 'PEIXE', larg/4 + 150, alt/2 + 200, 30)
    pick_radial = classes.Button(screen, 'AGUA VIVA', 3/4 * larg - 150, alt/2 + 200, 30)

    animals.add(bilaterio, radial, fundo)
    all_buttons.add(pick_radial, pick_bilaterio)

    while pick_run:
        clock.tick(30)
        click = False
        mx, my = pg.mouse.get_pos()

        # GET DE EVENTOS____________________________________________:
        for event in pg.event.get():
            # GAME QUIT_____________________________________________:
            if event.type == pg.QUIT:
                pg.quit()
                break

            # MOUSE CLICK___________________________________________:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

            # COLISAO DOS BOTOES____________________________________:
            if click:
                pick_bilaterio.clicked(mx, my)
                pick_radial.clicked(mx, my)

            if pick_bilaterio.update():
                pick_run = False
                screen.fill((40, 40, 40))
                game_loop('bilateral')

            if pick_radial.update():
                pick_run = False
                screen.fill((40, 40, 40))
                game_loop('radial')

        screen.fill((127, 205, 255))

        #
        bilaterio.rotate(bilaterio.x + 10, bilaterio.y)
        radial.rotate(radial.x, radial.y - 1)
        animals.update()

        all_buttons.draw(screen)
        animals.draw(screen)

        title.render_text()
        for but in all_buttons:
            but.render_text()

        # ATT DA TELA_______________________________________________:
        pg.display.update()
        pg.display.flip()


# GAME LOOP_________________________________________________________:
def game_loop(animal_tipo):
    game_run = True
    crabs = []
    death_time = 0

    # OBJETOS_______________________________________________________:
    points = classes.Points(screen)
    timer = classes.Tempo(screen)
    morreu = classes.GameOver(screen, larg, alt)

    if animal_tipo == 'radial':
        animal = classes.Radial(alt, larg, screen)
        pred = classes.Turtle(screen)
        crab_tipo = 'fish'
    else:
        animal = classes.Bilaterio(alt, larg, screen)
        pred = classes.Shark(screen)
        crab_tipo = 'shrimp'

    # SPRITES____________________________________________________:
    all_lighten = pg.sprite.Group()
    all_dark = pg.sprite.Group()
    death_group = pg.sprite.Group()
    all_lighten.add(animal, points, timer)
    all_dark.add(pred)
    for i in range(0, 5):
        crabt = classes.Crab(crab_tipo)
        crabs.append(crabt)
        all_dark.add(crabt)

    # MAIN LOOP_________________________________________________:
    while game_run:
        clock.tick(60)
        click = False
        mx, my = pg.mouse.get_pos()

        # EVENT GET_____________________________________________:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break

            # MOUSE CLICK GET____________________________________:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

        # MOUSE CLICK ACTION______________________________________:
        if click:
            morreu.main_menu.clicked(mx, my)

        if morreu.main_menu.update():
            game_run = False
            screen.fill((127, 205, 255))
            main_menu()

        screen.fill((0, 41, 52))

        # RENDER DO PREDADOR + CRABS______________________________:
        all_dark.draw(screen)

        # CHECK - ATT OS OBJETOS SE ESTIVER VIVO__________________:
        if animal.alive:
            pred.hunt(animal.x, animal.y)
            pred.move()
            pred.rotate()

            # RENDERIZA OS OBJETOS SEM LUZ_________________________:
            all_dark.update()

            # ATT DOS CRABS________________________________________:
            for crab in crabs:
                crab.move()
                if animal.eat(crab.collideRect):
                    # DELETA O CRAB COMIDO_________________________:
                    crab.kill()
                    crabs.remove(crab)
                    del crab
                    points.count += 1

                    # CRIA UM NOVO CRAB____________________________:
                    new_crab = classes.Crab(crab_tipo)
                    all_dark.add(new_crab)
                    crabs.append(new_crab)

            # ATUALIZA O ANIMAL____________________________________:
            animal.rotate(mx, my)
            animal.move(mx, my)
            animal.render_fog()

            # ATUALIZA OBJETOS ILUMINADOS__________________________:
            all_lighten.update()

            # CHECK DE MORTE (TEMPO)_______________________________:
            if timer.timer():
                animal.alive = False
                morreu.txt_render('tempo')
                death_group.add(morreu.main_menu)

            # CHECK DE MORTE (PREDADOR)____________________________:
            elif animal.death(pred.collideRect):
                if death_time == 20:
                    animal.alive = False
                    death_time = 0
                    morreu.txt_render('predado')
                    death_group.add(morreu.main_menu)

                death_time += 1
            else:
                death_time = 0

        # RENDER DOS OBJETOS ILUMINADOS____________________________:
        all_lighten.draw(screen)
        points.render_txt()
        timer.render_txt()

        # RENDER DA TELA DE GAME OVER______________________________:
        if not animal.alive:
            morreu.render()
            death_group.update()
            death_group.draw(screen)
            morreu.main_menu.render_text()

        # RENDER DA TELA___________________________________________:
        pg.display.update()
        pg.display.flip()


# START____________________________________________________________:
if __name__ == '__main__':
    main_menu()

pg.quit()
