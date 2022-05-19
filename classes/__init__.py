import os
import random
import pygame as pg
import math

# FONTES
pg.font.init()
font_30 = pg.font.Font('ARCADECLASSIC.TTF', 30)


# CONTAGEM DOS PONTOS________________________________________________:
class Points(pg.sprite.Sprite):
    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.count = 0
        self.screen = screen
        self.x = 100
        self.y = 74
        self.point_count = font_30.render(f'{self.count}', True, (255, 255, 255))
        self.render()

    def render(self):
        self.image = pg.image.load(os.path.join('images', 'hud1.png')).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def render_txt(self):
        self.point_count = font_30.render(f'{self.count}', True, (255, 255, 255))
        self.screen.blit(self.point_count, (95, 53))


# CONTAGEM DO TEMPO__________________________________________________:
class Tempo(pg.sprite.Sprite):
    def __init__(self, screen):
        pg.sprite.Sprite.__init__(self)
        self.time = 0
        self.screen = screen
        self.x = 162
        self.y = 74
        self.time_count = font_30.render(f'{self.time}', True, (250, 250, 250))
        self._render()

    def _render(self):
        self.image = pg.image.load(os.path.join('images', 'hud2.png')).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def timer(self):
        if self.time >= 7200:
            print(self.time)
            return True
        else:
            self.time += 1
            return False

    def render_txt(self):
        self.time_count = font_30.render(f'{120 - math.floor(self.time/60)}', True, (250, 250, 250))
        self.screen.blit(self.time_count, (140, 53))


# PERSONAGEM JOGAVEL_________________________________________________:
class Animal(pg.sprite.Sprite):
    def __init__(self, alt, larg, screen):
        pg.sprite.Sprite.__init__(self)
        self.xvet = 0
        self.yvet = 0
        self.fov_rect = None
        self.fov = None
        self.original_fov = None
        self.fog = None
        self.collideRect = None
        self.original_image = None
        self.alive = True
        self.screen = screen
        self.x = larg / 2
        self.y = alt / 2

        # FOV
        self.FOG_COLOR = (0, 0, 0)
        self.LIGHT_RADIUS = (0, 0)
        self.LIGHT_MASK = 'Elipse.png'

        # VEL. DE MOVIMENTACAO
        self.velmult = 0

    def render(self, img):
        # Criacao do sprite
        a = pg.image.load(img).convert()
        self.original_image = pg.transform.scale(a, (128, 168))
        self.original_image.set_colorkey((0, 177, 64))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Rect especifico de colisao
        self.collideRect = pg.rect.Rect((0, 0), (80, 80))
        self.collideRect.center = self.rect.center

    def fog_render(self, larg, alt):
        # Criacao da fog e fov
        self.fog = pg.Surface((larg, alt))
        self.fog.fill(self.FOG_COLOR)
        self.original_fov = pg.image.load(self.LIGHT_MASK).convert_alpha()
        self.original_fov = pg.transform.scale(self.original_fov, self.LIGHT_RADIUS)
        self.fov = self.original_fov
        self.fov_rect = self.fov.get_rect()

    def vetor(self, mx, my):
        vec_x, vec_y = mx - self.x, my - self.y
        return vec_x, vec_y

    def move(self, mx, my):
        if self.move_check(mx, my):
            self.xvet, self.yvet = self.vetor(mx, my)
            hip = math.sqrt((self.xvet ** 2) + (self.yvet ** 2))  # hipotenusa h^2 = ca^2 + co^2
            xvel = self.xvet / hip  # coseno cos = co / hip
            yvel = self.yvet / hip  # seno sin = ca / hip

            self.x += xvel * self.velmult
            self.y += yvel * self.velmult

    # Rotacao do sprite e do FOV
    def rotate(self, mx, my):
        vec_x, vec_y = self.vetor(mx, my)
        # (180/math.pi)* pq calcula em radianos e precisa de graus. negativo pq calcula na direcao oposta
        angle = (180 / math.pi) * -math.atan2(vec_y, vec_x)  # Y ANTES DE X!!!

        if self.xvet < 0:
            self.image = pg.transform.rotate(self.original_image, int(angle) + 180)

        elif self.xvet >= 0:
            self.image = pg.transform.rotate(self.original_image, int(angle))

        self.fov = pg.transform.rotate(self.original_fov, int(angle) - 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collideRect.center = self.rect.center
        self.fov_rect = self.fov.get_rect()

    def move_check(self, mx, my):
        if math.floor(self.x) == mx or math.ceil(self.x) == mx:
            return False

        elif math.floor(self.y) == my or math.ceil(self.y) == my:
            return False

        else:
            return True

    # Desenha a FOG
    def render_fog(self):
        self.fog.fill(self.FOG_COLOR)
        self.fov_rect.center = (self.x, self.y)
        self.fog.blit(self.fov, self.fov_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def death(self, pred_colliderect):
        if self.collideRect.colliderect(pred_colliderect):
            return True

    def eat(self, food_rect):
        if self.collideRect.colliderect(food_rect):
            return True


# BILATERAL__________________________________________________________:
class Bilaterio(Animal):
    def __init__(self, alt, larg, screen):
        # INICIALIZADOR______________________________________________:
        Animal.__init__(self, alt, larg, screen)

        # VARIAVEIS__________________________________________________:
        self.LIGHT_RADIUS = (500, 1000)
        self.LIGHT_MASK = 'cone_fov.png'
        self.img = 'bagre_.png'
        self.velmult = 3

        # VARIAVEIS DE ANIMAÇÃO________________________________________________:
        self.images = []
        self.frame_count = 0

        # INICIALIZADORES____________________________________________:
        self.render(self.img)
        self.fog_render(larg, alt)

    def render(self, img):
        # LOAD DOS ARQUIVOS____________________________________________________:
        self.images = []
        self.images.append(pg.image.load(os.path.join('images', 'fish1.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'fish2.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'fish3.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'fish4.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'fish5.png')).convert())

        self.original_image = self.images[0]
        self.original_image = pg.transform.scale(self.original_image, (128, 168))

        self.original_image.set_colorkey((0, 177, 64))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Rect especifico de colisao
        self.collideRect = pg.rect.Rect((0, 0), (80, 80))
        self.collideRect.center = self.rect.center

    def update(self):
        self.original_image = self.images[math.floor(self.frame_count)]
        self.original_image = pg.transform.scale(self.original_image, (128, 128))
        self.original_image = pg.transform.flip(self.original_image, True, False) if self.xvet < 0 else pg.transform.\
            flip(self.original_image, False, False)
        self.original_image.set_colorkey((0, 177, 64))
        self.frame_count += 0.2
        if self.frame_count >= 4:
            self.frame_count = 0


class Radial(Animal):
    def __init__(self, alt, larg, screen):
        # INICIALIZADOR______________________________________________:
        Animal.__init__(self, alt, larg, screen)

        # VARIAVEIS__________________________________________________:
        self.images = None
        self.LIGHT_RADIUS = (500, 500)
        self.LIGHT_MASK = 'Elipse.png'
        self.img = 'crab.png'
        self.velmult = 2
        self.frame_count = 0

        # INICIALIZADORES____________________________________________:
        self.render(self.img)
        self.fog_render(larg, alt)

    def render(self, img):
        # LOAD DOS ARQUIVOS____________________________________________________:
        self.images = []
        self.images.append(pg.image.load(os.path.join('images', 'jellyfish1.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'jellyfish2.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'jellyfish3.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'jellyfish4.png')).convert())

        self.original_image = self.images[0]
        self.original_image = pg.transform.scale(self.original_image, (64, 64))

        self.original_image.set_colorkey((0, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Rect especifico de colisao
        self.collideRect = pg.rect.Rect((0, 0), (40, 40))
        self.collideRect.center = self.rect.center

    def update(self):
        self.original_image = self.images[math.floor(self.frame_count)]
        self.original_image = pg.transform.scale(self.original_image, (64, 64))
        self.original_image = pg.transform.flip(self.original_image, True, False) if self.xvet < 0 else pg.transform.\
            flip(self.original_image, False, False)
        self.original_image.set_colorkey((0, 0, 0))
        self.frame_count += 0.2
        if self.frame_count >= 4:
            self.frame_count = 0

    # Rotacao do sprite e do FOV
    def rotate(self, mx, my):
        #  if self.move_check(mx, my):
        vec_x, vec_y = self.vetor(mx, my)
        # (180/math.pi)* pq calcula em radianos e precisa de graus. negativo pq calcula na direcao oposta
        angle = (180 / math.pi) * -math.atan2(vec_y, vec_x) - 90  # Y ANTES DE X!!!
        self.image = pg.transform.rotate(self.original_image, int(angle))
        self.fov = pg.transform.rotate(self.original_fov, int(angle))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collideRect.center = self.rect.center
        self.fov_rect = self.fov.get_rect()


# PREDADOR___________________________________________________________:
class Apex(pg.sprite.Sprite):
    def __init__(self, screen, tipo):
        pg.sprite.Sprite.__init__(self)
        self.collideRect = None
        self.original_image = None
        self.screen = screen
        self.x = random.randint(0, 1280)
        self.y = random.randint(0, 720)
        self.prey_x = int
        self.prey_y = int
        self.hunting = False
        self.moving = False
        self.targetx = int
        self.targety = int
        self.velmult = 0
        self.hunt_time = 0
        self.tipo = tipo
        self.rotate_fix = 0

    def render(self):
        self.original_image = pg.image.load(os.path.join('images', f'{self.tipo}.png')).convert()
        self.original_image = pg.transform.scale(self.original_image, (100, 100))
        self.original_image.set_colorkey((0, 177, 64))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.collideRect = pg.rect.Rect((0, 0), (80, 80))
        self.collideRect.center = self.rect.center

    # Movimentacao quando nao estiver caçando
    def move(self):
        if not self.hunting:
            if not self.moving:
                self.targetx, self.targety = random.randint(0, 1280), random.randint(0, 720)
                self.moving = True

            # Muda o destino quando chega no atual
            if math.floor(self.x) == self.targetx or math.ceil(self.x) == self.targetx:
                self.targetx, self.targety = random.randint(0, 1280), random.randint(0, 720)

            elif math.floor(self.y) == self.targety or math.ceil(self.y) == self.targety:
                self.targetx, self.targety = random.randint(0, 1280), random.randint(0, 720)

        elif self.hunting:
            pass

        # Calcula a rota e velocidade de acordo com o targetx e targety
        xvet, yvet = self.vetor(self.targetx, self.targety)
        hip = math.sqrt((xvet ** 2) + (yvet ** 2))  # hipotenusa h^2 = ca^2 + co^2
        xvel = xvet / hip  # coseno cos = co / hip
        yvel = yvet / hip  # seno sin = ca / hip
        self.x += xvel * self.velmult
        self.y += yvel * self.velmult

    # Calculo dos vetores
    def vetor(self, x, y):
        vec_x, vec_y = x - self.x, y - self.y
        return vec_x, vec_y

    # Check e movimentaçao quando caçando
    def hunt(self, prey_x, prey_y):
        distx, disty = self.vetor(prey_x, prey_y)
        if abs(distx) < 200 and abs(disty) < 200:
            if self.hunt_time <= 300:
                self.hunting = True
                self.moving = False
                self.targetx = prey_x
                self.targety = prey_y
                self.hunt_time += 1

            elif self.hunt_time <= 420:
                self.hunting = False

            else:
                self.hunt_time = 0

        else:
            self.hunting = False
            self.hunt_time = 0

    def rotate(self):
        vec_x, vec_y = self.vetor(self.targetx, self.targety)
        angle = (180 / math.pi) * -math.atan2(vec_y, vec_x)  # Y ANTES DE X!!!
        self.image = pg.transform.rotate(self.original_image, int(angle) + self.rotate_fix)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collideRect.center = self.rect.center


class Turtle(Apex):
    def __init__(self, screen):
        Apex.__init__(self, screen, 'turtle')
        self.rotate_fix = 180
        self.velmult = 2
        self.render()


class Shark(Apex):
    def __init__(self, screen):
        Apex.__init__(self, screen, 'shark')
        self.velmult = 3
        self.render()


# COMIDA_____________________________________________________________:
class Crab(pg.sprite.Sprite):
    def __init__(self, tipo):
        pg.sprite.Sprite.__init__(self)
        self.collideRect = None
        self.x = random.randint(0, 1280)
        self.y = random.randint(0, 720)
        self.targetx = random.randint(0, 1280)
        self.targety = random.randint(0, 720)
        self.velmult = 1.5
        self.moving = True
        self.time_stead = 0
        self.tipo = tipo
        self.render()

    def render(self):
        self.image = pg.image.load(os.path.join('images', f'{self.tipo}1.png')).convert()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.image.set_colorkey((0, 177, 64))
        self.rect = self.image.get_rect()
        self.collideRect = pg.rect.Rect((self.x, self.y), (10, 10))
        self.rect.center = self.x, self.y
        self.collideRect.center = self.x, self.y

    # Calculo dos vetores
    def vetor(self, x, y):
        vec_x, vec_y = x - self.x, y - self.y
        return vec_x, vec_y

    def move(self):
        # Muda o destino quando chega no atual
        if math.floor(self.x) == self.targetx or math.ceil(self.x) == self.targetx:
            if self.time_stead >= 300:
                self.targetx, self.targety = random.randint(0, 1280), random.randint(0, 720)
                self.time_stead = 0
                self.moving = True
            else:
                self.time_stead += 1
                self.moving = False

        elif math.floor(self.y) == self.targety or math.ceil(self.y) == self.targety:
            if self.time_stead >= 300:
                self.targetx, self.targety = random.randint(0, 1280), random.randint(0, 720)
                self.time_stead = 0
                self.moving = True
            else:
                self.time_stead += 1
                self.moving = False

        if self.moving:
            # Calcula a rota e velocidade de acordo com o targetx e targety
            xvet, yvet = self.vetor(self.targetx, self.targety)
            hip = math.sqrt((xvet ** 2) + (yvet ** 2))  # hipotenusa h^2 = ca^2 + co^2
            xvel = xvet / hip  # coseno cos = co / hip
            yvel = yvet / hip  # seno sin = ca / hip
            self.x += xvel * self.velmult
            self.y += yvel * self.velmult

            self.rect.center = self.x, self.y
            self.collideRect.center = self.x, self.y


# BOTAO______________________________________________________________:
class Button(pg.sprite.Sprite):
    def __init__(self, screen, name, x, y, font_size):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font('ARCADECLASSIC.TTF', font_size)
        self.name = name
        self.screen = screen
        self.x = x
        self.y = y

        # LOAD DOS ARQUIVOS____________________________________________________:
        self.images = []
        self.images.append(pg.image.load(os.path.join('images', 'button.png')).convert())
        self.images.append(pg.image.load(os.path.join('images', 'button_pressed.png')).convert())

        # VARIAVEIS DE ANIMAÇÃO________________________________________________:
        self.count = 0
        self.pressed = False
        self.start_count = False
        self.resp = False

        # CRIAÇÃO DO SPRITE DO BOTÃO___________________________________________:
        self.image = self.images[0]
        self.image.set_colorkey((0, 177, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Texto do botão_______________________________________________________:
        self.text = self.font.render(self.name, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_x = self.x - self.text_rect.width / 2
        self.text_y = self.y - self.text_rect.height / 2

    # CHECK DE COLISAO_________________________________________________________:
    def clicked(self, mx, my):
        if self.rect.collidepoint(mx, my):
            self.start_count = True

    # ANIMAÇÃO DO BOTÃO________________________________________________________:
    def update(self):
        # GARANTE QUE O SPRITE 2 DO BOTÃO NÃO PASSE MUITO RÁPIDO_______________:
        if self.start_count:
            self.image = self.images[1]
            if self.count >= 1:
                self.count = 0
                self.start_count = False
                self.resp = True

            self.image.set_colorkey((0, 0, 0))
            self.count += 0.25

        else:
            self.image = self.images[0]
            self.image.set_colorkey((0, 0, 0))

        return self.resp

    # RENDER DO TEXTO DO BOTÃO_________________________________________________:
    def render_text(self):
        self.screen.blit(self.text, (self.text_x, self.text_y))


class GameOver(pg.sprite.Sprite):
    def __init__(self, screen, larg, alt):
        pg.sprite.Sprite.__init__(self)

        # VARIAVEIS ___________________________________________________________:
        self.text2_y = None
        self.text2_x = None
        self.text2_rect = None
        self.text2 = None
        self.screen = screen
        self.font60 = pg.font.Font('ARCADECLASSIC.TTF', 100)
        self.font30 = pg.font.Font('ARCADECLASSIC.TTF', 25)
        self.text_y = None
        self.text_x = None
        self.text_rect = None
        self.text = None
        self.fog = None
        self.x = larg / 2
        self.y = alt / 2
        self.FOG_COLOR = (50, 125, 175)
        self.main_menu = Button(self.screen, 'Menu Principal', self.x, self.y + 200, 22)

        # INICIALIZADORES______________________________________________________:
        self.fog_render(larg, alt)

    def fog_render(self, larg, alt):
        self.fog = pg.Surface((larg, alt))
        self.fog.fill(self.FOG_COLOR)

    def txt_render(self, morte_tipo):
        # TEXTO________________________________________________________________:
        self.text = self.font60.render('GAME OVER', True, (210, 210, 210))
        self.text_rect = self.text.get_rect()
        self.text_x = self.x - self.text_rect.width / 2
        self.text_y = self.y - self.text_rect.height / 2 - 200

        if morte_tipo == 'predado':
            self.text2 = self.font30.render('Voce foi predado!', True, (210, 210, 210))
        else:
            self.text2 = self.font30.render('Tempo acabou', True, (210, 210, 210))

        self.text2_rect = self.text2.get_rect()
        self.text2_x = self.x - self.text2_rect.width / 2
        self.text2_y = self.y - self.text2_rect.height / 2 - 130

    # Desenha a FOG
    def render_fog(self):
        self.fog.fill(self.FOG_COLOR)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def render_text(self):
        self.screen.blit(self.text, (self.text_x, self.text_y))
        self.screen.blit(self.text2, (self.text2_x, self.text2_y))

    def render(self):
        self.render_fog()
        self.render_text()


class Fundo(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.x = 1280/2 -5
        self.y = 100
        self.image = pg.image.load(os.path.join('images', 'hud1.png')).convert()
        self.image = pg.transform.scale(self.image, (256*10, 156))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Mirror(pg.sprite.Sprite):
    def __init__(self, x, y, tipo):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.image.load(os.path.join('images', 'mirror.png')).convert()
        if tipo:
            self.image = pg.transform.flip(self.image, True, False)
        self.image = pg.transform.scale(self.image, (156, 156))
        self.image.set_colorkey((0, 177, 64))
        self.rect = self.image.get_rect(center=(self.x, self.y))
