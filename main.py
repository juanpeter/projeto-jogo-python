import pygame, random
from pygame.locals import *

################################################################
#CONFIGURAÇÕES PRINCIPAIS
TITLE = 'Escape the House'
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 288
FPS = 30

#Velocidade do protag
CHAR_WIDTH, CHAR_HEIGHT = ((32),(32))
SPEED = 4

#Medidas do ground
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

#Medidas da Pipe
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200

#gravidade
GRAVITY = 1
#velocidade horizontal do jogo
GAME_SPEED = 10

#Criar classe Protag, o personagem principal
class Protag(pygame.sprite.Sprite):

    #código de inicialização de toda classe Sprite do pygame
    def __init__(self):
        #inicializar sprite
        pygame.sprite.Sprite.__init__(self)

        #Trocar apenas as sprites de acordo com o movimento
        self.images = [
            #front
            pygame.image.load('assets/personagens/protagonista/front.png').convert_alpha(),
            #back
            pygame.image.load('assets/personagens/protagonista/back.png').convert_alpha(),
            #Side NOTA: Sempre está a direita, usar flip()
            pygame.image.load('assets/personagens/protagonista/side1.png').convert_alpha(),
            pygame.image.load('assets/personagens/protagonista/side2.png').convert_alpha(),
        ]
        # Tamanho das sprites
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (CHAR_WIDTH, CHAR_HEIGHT))

        #Velocidade
        self.speed = SPEED

        #A função convert_alpha faz imagens png serem transparentes
        self.image = self.images[0]
        #Criar máscara de colisão
        self.mask = pygame.mask.from_surface(self.image)
        #Necessário para posicionar a sprite na tela
        self.rect = self.image.get_rect()
        #Desenhar o pássaro na metade da tela. o [0] se refere a posição X
        self.rect[0] = SCREEN_WIDTH / 2
        #Desenhar o pássaro na metade da tela. o [1] se refere a posição Y
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):

        #controles do jogador
        control = pygame.key.get_pressed()
        if control[pygame.K_UP]:
            self.image = self.images[1]
            protag.rect[1] -= SPEED
        if control[pygame.K_DOWN]:
            self.image = self.images[0]
            protag.rect[1] += SPEED
        if control[pygame.K_LEFT]:
            self.image = self.images[3]
            #Achar maneira de saber que a tecla CONTINUA
            #sendo precionada, para alterar a sprite
            
            #Virar a imagem para a esquerda
            self.image = pygame.transform.flip(self.image, True, False)
            protag.rect[0] -= SPEED
        if control[pygame.K_RIGHT]:
            self.image = self.images[3]
            protag.rect[0] += SPEED

    
    def walk(self):
        print('andou!')
        

#Criar classe Ground, bg que acompanha o personagem
# class Ground(pygame.sprite.Sprite):

#     # a classe Ground() pode ter sua posição definida durante sua execução (xpos)
#     def __init__(self, xpos):
#         #inicializar sprite
#         pygame.sprite.Sprite.__init__(self)

#         #load na imagem do ground
#         self.image = pygame.image.load('assets/base.png').convert_alpha()
#         #Criar máscara de colisão
#         self.mask = pygame.mask.from_surface(self.image)
#         #tamanhos da imagem do ground
#         self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
#         #pegar posição da imagem
#         self.rect = self.image.get_rect()
#         #Ground começa onde é invocado durante a função
#         self.rect[0] = xpos
#         #Ground fica no fundo da tela
#         self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

#     def update(self):
#         #mover o ground junto com o jogo
#         self.rect[0] -= GAME_SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        #inicializar sprite
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()

        self.rect[0] = xpos

        #inverter a pipe, se necessário
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


#Função para verificar se a sprite está fora da tela
def is_of_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

#Função para criar canos aleatórios
def get_random_pipes(xpos):
    #Cani de tamanho aleatório
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)

# Inicializador do jogo
pygame.init()

#display do nome do jogo
pygame.display.set_caption(TITLE)

#configurações de tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/ambientes/quarto/room.png')

#A imagem de bg terá o tamanho (SCREEN_WIDTH, SCREEN_HEIGHT)
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Criar um grupo de passaros, criar um pássaro e adicioná-lo no grupo
protag_group = pygame.sprite.Group()
protag = Protag()
protag_group.add(protag)

#Criar grupo do Ground
# ground_group = pygame.sprite.Group()

# O xpos irá loopar de maneira que o primeiro caso ele aparecerá em X 0,
# o segundo logo após a SCREEN_WIDTH pasasr e assim irá loopar
# for i in range(2):
#     # A largura do chão é o dobro da largura da tela
#     ground = Ground(GROUND_WIDTH * i)
#     ground_group.add(ground)


#Criar grupo de pipes
pipe_group = pygame.sprite.Group()

for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

#fps
clock = pygame.time.Clock()

while True:
    #definir fps no jogo
    clock.tick(FPS)

    #Loop básico
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            protag.walk()

    # criar imagem de BACKGROUND na posição 0,0
    screen.blit(BACKGROUND, (0,0))

    # if is_of_screen(ground_group.sprites()[0]):
        #se o ground estiver fora da visão, deletar esse ground
        # ground_group.remove(ground_group.sprites()[0])
        #criar novo ground, com -20 pxs de distância para parecer "infinito"
        # new_ground = Ground(GROUND_WIDTH - 20)
        #adicionar esse novo ground na tela
        # ground_group.add(new_ground)

    if is_of_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    # atualizar o grupo dos pássaros
    protag_group.update()

    #atualizar grupo do ground
    # ground_group.update()

    # pipe_group.update()

    #desenhar o grupo dos pássaros na tela
    protag_group.draw(screen)

    # pipe_group.draw(screen)

    #desenhar groupo ground na tela
    # ground_group.draw(screen)

    # se o pássaro colidir com o ground...
    # Importante, a função pygame.sprite.collide_mask faz com que apenas pixels
    # que não são transparentes contem para uma colisão
    if False:
        #O jogo acaba
        break

    pygame.display.update()