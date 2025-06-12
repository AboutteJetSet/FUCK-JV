import pygame
import sys

pygame.init()

# sdsss
largura, altura = 1200, 850
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("SPRA8")

fonte = pygame.font.SysFont("Comic Sans MS", 50)
clock = pygame.time.Clock()

#texto
def desenha_texto(texto, cor, x, y):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=(x, y))
    tela.blit(render, rect)

#fade
def fade_transicao(duracao=500):
    fade = pygame.Surface((largura, altura))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(duracao // 25)

#botão do pause
def carregar_botoes_pause():
    spritesheet = pygame.image.load("SPRA8/spritees/bottom/BOTÕES.png").convert_alpha()

    
    colunas = 3
    linhas = 4

    largura_total, altura_total = spritesheet.get_size()
    largura_botao = largura_total // colunas  
    altura_botao = altura_total // linhas     

    escala = 0.5  # Reduzir tamanho dos botões

    botoes = {}

    botoes_info = {
        "Continue": 2, 
        "Exit": 3     
    }

    for nome, linha in botoes_info.items():
        normal_rect = pygame.Rect(0 * largura_botao, linha * altura_botao, largura_botao, altura_botao)
        sel_rect = pygame.Rect(1 * largura_botao, linha * altura_botao, largura_botao, altura_botao)

        normal = spritesheet.subsurface(normal_rect)
        selecionado = spritesheet.subsurface(sel_rect)

        # Redimensionar
        normal = pygame.transform.scale(normal, (int(largura_botao * escala), int(altura_botao * escala)))
        selecionado = pygame.transform.scale(selecionado, (int(largura_botao * escala), int(altura_botao * escala)))

        botoes[nome] = {
            "normal": normal,
            "selecionado": selecionado
        }

    return botoes
#sprite DeltA
def carregar_frames():
    sprite_sheet = pygame.image.load("SPRA8/spritees/personas/sprite_DeltA.png").convert_alpha()

    frame_width = sprite_sheet.get_width() // 4
    frame_height = sprite_sheet.get_height() // 4

    escala = 0.5
    novo_largura = int(frame_width * escala)
    novo_altura = int(frame_height * escala)

    animacoes = {
        "baixo": [],
        "cima": [],
        "esquerda": [],
        "direita": []
    }

    direcoes = ["baixo", "cima", "esquerda", "direita"]

    for linha, direcao in enumerate(direcoes):
        for i in range(4):
            frame = sprite_sheet.subsurface(pygame.Rect(
                i * frame_width,
                linha * frame_height,
                frame_width,
                frame_height
            ))
            frame_redimensionado = pygame.transform.scale(frame, (novo_largura, novo_altura))
            animacoes[direcao].append(frame_redimensionado)

    return animacoes

#l0w k1ck
def carregar_frames_inimigo():
    spritesheet = pygame.image.load("SPRA8/spritees/personas/SPRITE LOW KICK.png").convert_alpha()
    
    largura_total = spritesheet.get_width()
    altura_total = spritesheet.get_height()

    frame_height = altura_total // 2
    frame_width = largura_total

    escala = 0.5  # <- mesma escala do personagem

    novo_largura = int(frame_width * escala)
    novo_altura = int(frame_height * escala)

    frame1 = spritesheet.subsurface(pygame.Rect(0, 0, frame_width, frame_height))
    frame2 = spritesheet.subsurface(pygame.Rect(0, frame_height, frame_width, frame_height))

    frame1 = pygame.transform.scale(frame1, (novo_largura, novo_altura))
    frame2 = pygame.transform.scale(frame2, (novo_largura, novo_altura))

    return [frame1, frame2]

#enemys
class Inimigo:
    def __init__(self, x, y):
        self.frames = carregar_frames_inimigo()
        self.frame_index = 0
        self.timer = 0
        self.intervalo = 500  # asd
        self.x = x
        self.y = y
        self.largura = self.frames[0].get_width()
        self.altura = self.frames[0].get_height()

    def atualizar(self, tempo_atual):
        if tempo_atual - self.timer > self.intervalo:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.timer = tempo_atual

    def desenhar(self, tela):
        tela.blit(self.frames[self.frame_index], (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

#pouse
def pausar():
    opcoes = ["Continue", "Exit"]
    indice = 0
    pausado = True

    botoes = carregar_botoes_pause()

    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    indice = (indice - 1) % len(opcoes)
                elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                    indice = (indice + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if opcoes[indice] == "Continue":
                        pausado = False
                    elif opcoes[indice] == "Exit":
                        pygame.quit()
                        sys.exit()

        overlay = pygame.Surface((largura, altura))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        # Retângulo de fundo do menu
        menu_largura, menu_altura = 500, 300
        menu_x = (largura - menu_largura) // 2
        menu_y = (altura - menu_altura) // 2
        pygame.draw.rect(tela, (40, 40, 40), (menu_x, menu_y, menu_largura, menu_altura), border_radius=15)
        pygame.draw.rect(tela, (100, 100, 100), (menu_x, menu_y, menu_largura, menu_altura), width=4, border_radius=15)

        for i, opcao in enumerate(opcoes):
            imagem = botoes[opcao]["selecionado"] if i == indice else botoes[opcao]["normal"]
            x = (largura - imagem.get_width()) // 2
            y = menu_y + 80 + i * (imagem.get_height() + 20)
            tela.blit(imagem, (x, y))

        pygame.display.flip()
        clock.tick(30)

#menu
def menu_principal():
    opcoes = ["Start", "Exit"]
    indice = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    indice = (indice - 1) % len(opcoes)
                elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                    indice = (indice + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if opcoes[indice] == "Start":
                        fade_transicao()
                        return
                    elif opcoes[indice] == "Exit":
                        pygame.quit()
                        sys.exit()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        tela.fill((15, 15, 15))
        desenha_texto("SPRA8", (255, 255, 255), largura // 2, 150)

        for i, opcao in enumerate(opcoes):
            cor = (250, 168, 2) if i == indice else (200, 200, 200)
            desenha_texto(opcao, cor, largura // 2, 300 + i * 100)

        pygame.display.flip()

#tela do menu de estilo
def tela_menu():
    opcoes = ["goofy", "regular"]
    indice = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    indice = (indice - 1) % 2
                elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                    indice = (indice + 1) % 2
                elif evento.key == pygame.K_RETURN:
                    fade_transicao()
                    return opcoes[indice]
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        tela.fill((20, 20, 20))
        desenha_texto("Escolha seu estilo:", (255, 255, 255), largura // 2, 150)

        cor_goofy = (250, 168, 2) if indice == 0 else (255, 255, 255)
        cor_regular = (250, 168, 2) if indice == 1 else (255, 255, 255)

        desenha_texto("Goofy ( Setas )", cor_goofy, largura // 2, 270)
        desenha_texto("Regular ( WASD )", cor_regular, largura // 2, 350)

        pygame.display.flip()

#main game
def main_game(estilo):
    animacoes = carregar_frames()
    direcao = "baixo"
    frame_index = 0
    frame_timer = 0
    frame_interval = 150

    delta_x, delta_y = 100, 100
    velocidade = 3
    usar_setas = (estilo == "goofy")

    # === INIMIGO ===
    sprite_inimigo = pygame.image.load("SPRA8/spritees/personas/SPRITE LOW KICK.png").convert_alpha()
    inimigo_frames = []

    inimigo_escala = 0.6  # Reduz o tamanho do inimigo
    frame_height = sprite_inimigo.get_height() // 2
    frame_width = sprite_inimigo.get_width()

    for i in range(2):
        frame = sprite_inimigo.subsurface(pygame.Rect(0, i * frame_height, frame_width, frame_height))
        frame = pygame.transform.scale(
            frame, (int(frame_width * inimigo_escala), int(frame_height * inimigo_escala))
        )
        inimigo_frames.append(frame)

    inimigo_x, inimigo_y = 400, 300
    inimigo_index = 0
    inimigo_timer = 0
    inimigo_intervalo = 500

    rodando = True
    while rodando:
        tempo = pygame.time.get_ticks()
        movendo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                pausar()

        teclas = pygame.key.get_pressed()

        if usar_setas:
            if teclas[pygame.K_LEFT]:
                delta_x -= velocidade
                direcao = "esquerda"
                movendo = True
            elif teclas[pygame.K_RIGHT]:
                delta_x += velocidade
                direcao = "direita"
                movendo = True
            elif teclas[pygame.K_UP]:
                delta_y -= velocidade
                direcao = "cima"
                movendo = True
            elif teclas[pygame.K_DOWN]:
                delta_y += velocidade
                direcao = "baixo"
                movendo = True
        else:
            if teclas[pygame.K_a]:
                delta_x -= velocidade
                direcao = "esquerda"
                movendo = True
            elif teclas[pygame.K_d]:
                delta_x += velocidade
                direcao = "direita"
                movendo = True
            elif teclas[pygame.K_w]:
                delta_y -= velocidade
                direcao = "cima"
                movendo = True
            elif teclas[pygame.K_s]:
                delta_y += velocidade
                direcao = "baixo"
                movendo = True

        # Atualiza animação do jogador
        if movendo:
            if tempo - frame_timer > frame_interval:
                frame_index = (frame_index + 1) % 4 
                frame_timer = tempo
        else:
            frame_index = 0

        # Animação de "respirar" do inimigo
        if tempo - inimigo_timer > inimigo_intervalo:
            inimigo_index = (inimigo_index + 1) % len(inimigo_frames)
            inimigo_timer = tempo

        # === COLISÃO ===
        jogador_frame = animacoes[direcao][frame_index]
        jogador_rect = jogador_frame.get_rect(topleft=(delta_x, delta_y))
        inimigo_frame = inimigo_frames[inimigo_index]
        inimigo_rect = inimigo_frame.get_rect(topleft=(inimigo_x, inimigo_y))

        if jogador_rect.colliderect(inimigo_rect):
            print("Colidiu com o inimigo!")

        # === DESENHO ===
        tela.fill((30, 30, 30))
        tela.blit(jogador_frame, (delta_x, delta_y))
        tela.blit(inimigo_frame, (inimigo_x, inimigo_y))

        # DEBUG VISUAL DAS HITBOXES
        pygame.draw.rect(tela, (255, 0, 0), jogador_rect, 2)  # Vermelho: jogador
        pygame.draw.rect(tela, (0, 255, 0), inimigo_rect, 2)  # Verde: inimigo

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

menu_principal()
estilo_escolhido = tela_menu()
main_game(estilo_escolhido)

#// FUCK JÔAO VITOR FUCK