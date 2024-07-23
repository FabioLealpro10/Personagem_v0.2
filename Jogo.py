import pygame as pg
from pygame.locals import *
from sys import exit


pg.init()
altura = 600
largura = 800

branco = (250, 250, 250)

tela = pg.display.set_mode((largura, altura))
pg.display.set_caption('oooo7')


class personagem(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.movimentos = []
        for x in range(1, 3):  # 01 - 123456 - 78
            self.movimentos.append(pg.image.load(f'personagem/parado/parado{x}.png'))
        for x in range(1, 7):
            self.movimentos.append(pg.image.load(f'personagem/anda/anda{x}.png'))
        self.movimentos.append(pg.image.load('personagem/pulo/pulo.png'))
        self.movimentos.append(pg.image.load('personagem/agacha/agacha.png'))
        self.pulo = False
        self.esquerda = False
        self.atual = 0  # imagem que vai aparece na tela
        self.inicio_animacao = 0
        self.tamanho_animacao = 2
        self.local_x = 100
        self.local_y = 300
        self.image = self.movimentos[self.atual]  # image é atributa da class pygame
        self.rect = self.image.get_rect()
        self.tm_img_x = 34
        self.tm_img_y = 36
        self.rect.topleft = self.local_x, self.local_y
        self.image = pg.transform.scale(self.image, (self.tm_img_x, self.tm_img_y))

    def ficar_parado(self):
        self.tamanho_animacao = 2
        self.inicio_animacao = 0

    def andar(self):
        self.inicio_animacao = 2
        self.tamanho_animacao = 8

    def pular(self):
        self.pulo = True
        self.forsa_pulo = 1  # variavel pulo
        self.altura = 8
        self.atual = 8

    def agachamento(self):
        self.local_y = 311
        self.tm_img_x = 34
        self.tm_img_y = 25
        self.atual = 9
        self.inicio_animacao = 9
        self.tamanho_animacao = 10

    def update(self):
        if not (self.pulo):
            self.atual += 0.5
            if self.atual >= self.tamanho_animacao:
                self.atual = self.inicio_animacao
        else:
            if self.forsa_pulo < self.altura:
                self.local_y -= 3
                self.forsa_pulo += 1
            elif self.altura <= self.forsa_pulo <= self.altura + 1:
                self.forsa_pulo += 1
            else:
                self.local_y += 3
                if self.local_y == 300:
                    self.pulo = False

        self.image = self.movimentos[int(self.atual)]
        self.rect.topleft = self.local_x, self.local_y
        self.image = pg.transform.scale(self.image, (self.tm_img_x, self.tm_img_y))
        self.image = pg.transform.flip(self.image, self.esquerda, False)
        self.tm_img_y = 36
        if not (self.pulo):
            self.local_y = 300


class Bala(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.atira = False
        self.bala_lista = []
        for x in range(1, 4):
            i_bala = pg.image.load(f'personagem/bala/00{x}.png')
            self.bala_lista.append(i_bala)

        self.id_bala = 0
        self.image = self.bala_lista[self.id_bala]
        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100
        self.image = pg.transform.flip(self.image, False, False)
        self.image = pg.transform.scale(self.image, (200, 13))
    def update(self, localizacao_x, localizacao_y, esquerda):
        # tiver munição
        self.id_bala += 1
        if self.id_bala >= len(self.bala_lista):
            self.id_bala = 0

        if esquerda:
            local_x = localizacao_x - 197
        else:
            local_x = localizacao_x + 25
        local_y = localizacao_y
        self.image = self.bala_lista[self.id_bala]
        self.rect.topleft = local_x, local_y + 15
        self.image = pg.transform.scale(self.image, (200, 13))
        self.image = pg.transform.flip(self.image, esquerda, False)
        self.atira = False

class Inimigo(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # carrega splits
        self.lista_anima = []
        for x in range(8): # parado
            self.lista_anima.append(pg.image.load(f'inimigo/parado/{x}.png')) # 0 ao 7 parado
        for x in range(8):
            self.lista_anima.append(pg.image.load(f'inimigo/andar/{x}.png')) # 8 ao 15 andando
        for x in range(8):
            self.lista_anima.append(pg.image.load(f'inimigo/atira_agachado/{x}.png')) # 16 ao 23 atira_agachado
        for x in range(8):
            self.lista_anima.append(pg.image.load(f'inimigo/atira_em_pe/{x}.png')) # 24 ao 31 atira em pe
        for x in range(8):
            self.lista_anima.append(pg.image.load(f'inimigo/merreu/{x}.png')) # 32 ao 39 morreu

        self.dimecao_x = 49
        self.dimecao_y = 60

        self.apontar = False
        self.iniciar_animacao = 0
        self.finalizar_animacao = 8
        self.indice = 0
        self.image = self.lista_anima[self.indice]
        self.rect = self.image.get_rect()
        self.rect.topleft = 200, 300
        self.image = pg.transform.flip(self.image, self.apontar, False)
        self.image = pg.transform.scale(self.image, (self.dimecao_x//2,self.dimecao_y//2))

    def parado(self):
        self.iniciar_animacao = 0
        self.finalizar_animacao = 8
        self.indice = self.iniciar_animacao
        self.dimecao_x = 49
        self.dimecao_y = 60

    def andar(self):
        self.iniciar_animacao = 8
        self.finalizar_animacao = 15
        self.indice = self.iniciar_animacao
        self.dimecao_x = 49
        self.dimecao_y = 60


    def atira_em_pe(self):
        self.iniciar_animacao = 24
        self.finalizar_animacao = 31
        self.indice = self.iniciar_animacao
        self.dimecao_x = 73
        self.dimecao_y = 61

    def atira_agachado(self):
        self.iniciar_animacao = 16
        self.finalizar_animacao = 23
        self.indice = self.iniciar_animacao
        self.dimecao_x = 90
        self.dimecao_y = 51

    def morrer(self):
        self.iniciar_animacao = 32
        self.finalizar_animacao = 39
        self.indice = self.iniciar_animacao
        self.dimecao_x = 66
        self.dimecao_y = 46


    def update(self):
        self.indice += 0.5
        if int(self.indice) > self.finalizar_animacao:
            self.indice = self.iniciar_animacao

        self.image = self.lista_anima[int(self.indice)]
        self.rect = self.image.get_rect()
        self.rect.topleft = 200, 300
        self.image = pg.transform.flip(self.image, self.apontar, False)
        self.image = pg.transform.scale(self.image, (self.dimecao_x//2, self.dimecao_y//2))


        # troca de splits
        # dimencões das sprites
        # logica para muda as sprites
        pass


todas_as_splites = pg.sprite.Group()
personagem = personagem()
todas_as_splites.add(personagem)



image_bala = pg.sprite.Group()
bala = Bala()
image_bala.add(bala)
agacha = 0




splites_inimigo = pg.sprite.Group()
inimigo = Inimigo()
splites_inimigo.add(inimigo)


inimigo.atira_agachado()

relogio = pg.time.Clock()


while True:
    relogio.tick(20)
    tela.fill(branco)
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:
            if pg.key.get_pressed()[K_z] and not (personagem.pulo):
                personagem.pular()

            if pg.key.get_pressed()[K_x]:
                bala.update(personagem.local_x, personagem.local_y + agacha, personagem.esquerda)
                image_bala.draw(tela)
    if bala.atira:
        x = personagem.local_x
        y = personagem.local_y
        esq = personagem.esquerda
        image_bala.draw(tela)
        bala.update(x, y, esq)

    if pg.key.get_pressed()[K_RIGHT]:
        personagem.andar()
        personagem.esquerda = False
        personagem.local_x += 2

    elif pg.key.get_pressed()[K_LEFT]:
        personagem.andar()
        personagem.esquerda = True
        personagem.local_x -= 2

    elif pg.key.get_pressed()[K_DOWN] and not (personagem.pulo):
        personagem.agachamento()
        agacha = 5

    elif not (personagem.pulo):
        personagem.ficar_parado()
        agacha = 0

    todas_as_splites.draw(tela)
    todas_as_splites.update()

    splites_inimigo.draw(tela)
    splites_inimigo.update()

    pg.display.flip()
    # original FLP




