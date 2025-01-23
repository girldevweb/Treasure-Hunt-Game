import pygame



pygame.mixer.init()  # Inicializa o mixer

jump_sound = pygame.mixer.Sound('game/sounds/jump.mp3')
hit_sound = pygame.mixer.Sound('game/sounds/hit.mp3')
attack_sound = pygame.mixer.Sound('game/sounds/ataque.wav')
collect_sound = pygame.mixer.Sound('game/sounds/coletar.mp3')



GameSettings = {
    "TILE_SIZE": 50,
    "WINDOW_WIDTH": 900,
    "WINDOW_HEIGHT": 600
}
# Configuração da janela

screen = pygame.display.set_mode((GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"]))
pygame.display.set_caption("Treasure Hunt")


# Clock para controlar o framerate
clock = pygame.time.Clock()

# Variável global de estado do jogo
game_over = 0

# Carregando as camadas do background



# Matriz do level1
world_data1 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, "D", 1],
[1, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
[1, 0, 0, 0, 10, 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
[1, 2, 0, 9, 9, 9, 9, 0, 0, 0, 0, 0, 9, 9, 9, 9, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1], 
[1, 2, 2, 4, 0, 0, 2, 2, 0, 0, 18, 2, 2, 2, 2, 0, 0, 0, 2, 1], 
[1, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,2, 2, 0, 0, 0, 1],
[1, 0, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 1, 2, 2, 2, "S", 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 7, 0, 14, 0, 0, 0, 0, 1, 1],  
[1, 0, 0, 9, 9, 9, 9, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, "S", 0, 1], 
[1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 18, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 7, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2,1], 
[1, 0, 0, 2, 0, 0, 0, 0, 2, 0, 12, 0, 0, 0, 0, 2, 0, 0, 1,1], 
[1, 0, 0, 0, 0, 0, 0, 2, 2,2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 11, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, "S", 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2,0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 1], 
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 1], 
[1, 1, 1, 1, 17, 0, 0, 15, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1], 
[1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 4, 5, 0, 8, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 3 = Duende
# 4 = Cogumelo
# 5 = Goblin
# S = Spike
# 7 = Potion
# 8 = Key
# 9 = Coin
# D = Door
# 10 = Goblin King
# 11 = Minotaur
# 12 = Sneak
# 13 = Brain
# 14 = Cacodaemon
# 15 = Ghoul
# 16 = Bat
# 17 = Blue Monster
# 18 = Olho

# B = Boss
# Nos world_data1, world_data2, world_data3
# F = Fire (Fogo)
# S = Spike (Espinho)
# R = Suriken (Estrela ninja)
# P = FloorSpikes (Espinhos do chão)


#mapa do mundo level2 
world_data2 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 11, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 13, 0, 0, 0, 1, 0, 0, 0, "R", 0, 0, 0, "R", 0, "D", 1], 
[1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1],
[1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 1],  
[1, 0, 0, 0, 0, 9, 9, 9, 9, 0, 0, 1, 2, 2, 0, 0, "S",2, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 0, 2, 0, 0, 1, 1], 
[1, 0, 2, 0, 14, 0, 11, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 9, 9, 9, 9, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 18, 2, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 0, 2, "S", 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1], 
[1, 0, 0, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1, 1], 
[1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 7, 1, 1], 
[1, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 1, 0, 16, 0, 0, 0, 0, 0,0, 0, 0, 2, 0, 0, 2, 2, 1], 
[1, 0, 0, 1, 2, 2, 2, 0, 0, 0, 18, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 14, 0, 0, 2, 2, 0, 0, 1, 1], 
[1, 0, 0, 0, "S", "S", 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 1], 
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, "R", 0, 0, 0, 0, 0, 2, 2, 1], 
[1, 2, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 2, 1, 1], 
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1], 
[1, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 18, 0, 0, 3, 0, 16, 1, 1, 1], 
[1, 8, 0, 0, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1], 
[1, 2, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1], 
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 9, 9, 9, 9, 0, 0, 1, 1], 
[1, "L", "L", "L", 1, 2, 2, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 2, 2, 2, 1, 0, 0, "R", 0, 2, 2, 2, "L", "L", "L", "L", 1], 
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 3 = Duende
# 4 = Cogumelo
# 5 = Goblin
# S = Spike
# 7 = Potion
# 8 = Key
# 9 = Coin
# D = Door
# 10 = Goblin King
# 11 = Minotaur
# 12 = Sneak
# 13 = Brain
# 14 = Cacodaemon
# 15 = Ghoul
# 16 = Bat
# 17 = Blue Monster
# 18 = Olho

# B = Boss
# Nos world_data1, world_data2, world_data3
# F = Fire (Fogo)
# S = Spike (Espinho)
# R = Suriken (Estrela ninja)
# P = FloorSpikes (Espinhos do chão)
# T = bau

#mapa do mundo level3
world_data3 = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 0, 0, 0, 0, 1],
[1, "S", 0, "S", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  
[1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "B", "T", 0, 1],
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2,2, 2, 2, 2, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 11, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 1], 
[1, 2, 2, 2, 2, 2,0 , 0,"S" , 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 11, 0, 13, 0, 0, 0, 0, 1], 
[1, 2, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0,2, 2, 2, 2, 2, 0, 1, 1], 
[1, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 1, 2, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 1], 
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 1], 
[1, 2, 0, 1, 13, 0, 14, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 1], 
[1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 15, 0, 0, 17, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 1], 
[1, 0, 0, 0, 0, 15, 0, 16, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1], 
[1, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 11, 0, 18, 0, 1, 1], 
[1, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1], 
[1, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 1], 
[1, 16, 0, 0, 17, 0, 0, 0, 0, 2, 2, 2, 2, 0, 9, 9, 9, 0, 0, 1], 
[1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 1], 
[1, 0, 0, 2, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1], 
[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 1, 0, "S", 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 2, 2, 2, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 9, 9, 9, 9, 2, 1], 
[1, 8, 2, 2, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 14, 0, 7, 0, 2, 1], 
[1, 2,0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 2, 1], 
[1, 1, 0, 0, 2, 2, 2, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 2, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 
[1, 1, 0, 0, 0, 0, 0, 0, 0, "S", 0, "S", 0, 0, 0, 1, 1, 1, 1, 1], 
[1, 2, "S", 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1], 
[1, 2, 2, 2, 0, 0, "R", 0, 1, 1, 1, 1, 2, 0, 0, "R", 0, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# B = Boss
# Nos world_data1, world_data2, world_data3
# F = Fire (Fogo)
# S = Spike (Espinho)
# R = Suriken (Estrela ninja)
# P = FloorSpikes (Espinhos do chão)











enemy_group = pygame.sprite.Group()




# Game loop
run = True
scroll = [0, 0]



























# ------------ Cores ------------
Colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "blue": (0, 121, 241),
    "light_blue": (0, 181, 255),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "gray": (128, 128, 128)
}

# ------------ Player Sprites ------------
Player_Sprites = {
    "idle": [f"game/sprites/player/idle_frames/idle-{i}.png" for i in range(1, 7)],
    "run": [f"game/sprites/player/run_frames/run-{i}.png" for i in range(1, 9)]
}

# ------------ Tiles ------------
Tiles = {
    "dirt": "game/tiles/dirt.png",
    "grass": "game/tiles/grass.png",
    "dirt2": "game/tiles/dirt2.png",
    "dirt3": "game/tiles/dirt3.png",
    "grass2": "game/tiles/grass2.png",
    "grass3": "game/tiles/grass3.png"
}

# ------------ Items ------------
Items = {
    "heart": "game/items/heart.png",
    "coin": "game/items/coin.png",
    "potion": "game/items/potion.png",
    "key": "game/items/key.png",
    "settings": "game/items/settingsb.png",
    "up": "game/items/up.png",
    "left": "game/items/left.png",
    "right": "game/items/right.png",
    "home": "game/items/home.png",
    "restart": "game/items/restart.png",
    "door_closed": "game/items/door_closed.png",
    "door_open": "game/items/door_open.png",
    "audio_on": "game/items/audio_on.png",
    "audio_off": "game/items/audio_off.png",
    "pause": "game/items/pause.png",
    "play": "game/items/play.png",
    "next": "game/items/next.png",
    "laser": "game/images/laser.png",
    "bau_open": "game/images/bau-tesouro.png",
    "bau_locked": "game/images/bau.png",
    "fire": "game/items/Fire.png",
    "spike": "game/items/spike.png",
    "suriken": "game/items/Suriken.png",
    "floor_spikes": "game/items/floor_spikes.png",
    "livro": "game/items/livro.png",
    "folha": "game/items/folha.jpg",
    "lava": "game/items/lava.png"

}
Final_Boss = {
    "boss": [f"game/sprites/enemies/boss_frames/boss_{i}.png" for i in range(1, 9)]
}
# ------------ Inimigos ------------
Enemies = {
    "mushroom": "game/sprites/enemies/cogumelo.png",
    "elf": "game/sprites/enemies/duende.png",
    "goblin": "game/sprites/enemies/goblin_walk.png"
}

# ------------ Sons ------------
Sounds = {
    "attack": "game/sounds/ataque.wav",
    "click": "game/sounds/click.wav",
    "collect": "game/sounds/coletar.mp3",
    "hit": "game/sounds/hit.mp3",
    "jump": "game/sounds/jump.mp3",
    "theme": "game/sounds/forest.wav",
    "theme2": "game/sounds/cave.wav",
    "theme3": "game/sounds/finale.wav",
    "treasure": "game/sounds/tesouro.wav",
    "type": "game/sounds/type.wav",
    "intro": "game/sounds/intro_music.mp3"
}

# ------------ Imagens ------------
Images = {
    "spike": "game/images/spike.png",
    "portal": "game/images/portal.png",
    "treasure": "game/images/bau-tesouro.png",
    "bg-menu": "game/images/bg-menu.png",
    "bg-level_select": "game/images/bg-levelselect.png"
   
}

Settings_Icons = {
    "audio_on": "game/items/audio_on.png",
    "audio_off": "game/items/audio_off.png",
    "home": "game/items/home.png",
    "restart": "game/items/restart.png",
    "pause": "game/items/pause.png",
    "play": "game/items/play.png",
    "settingsb": "game/items/settingsb.png"
}
# ------------ Backgrounds Floresta ------------
BackForest = {
   
    "layer1": "game/backforest/plx-1.png",
    "layer2": "game/backforest/plx-2.png",
    "layer3": "game/backforest/plx-3.png",
    "layer4": "game/backforest/plx-4.png",
    "layer5": "game/backforest/plx-5.png",
    "layer6": "game/backforest/plx-6.png",
    "layer7": "game/backforest/plx-7.png"
}




bg_layers = []
for i in range(1, 8):
    layer = pygame.image.load(BackForest[f"layer{i}"]).convert_alpha()
    layer = pygame.transform.scale(layer, (GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"]))
    bg_layers.append(layer)


# ------------ Backgrounds Caverna ------------
BackCaves = {
    "layer1": "game/backcaves/7.png",
    "layer2": "game/backcaves/6.png",
    "layer3": "game/backcaves/5.png",
    "layer4": "game/backcaves/4.png",
    "layer5": "game/backcaves/3.png",
    "layer6": "game/backcaves/2.png",
    "layer7": "game/backcaves/1.png"
   
}

# ------------ Backgrounds Templo ------------
BackTemple = {
    "layer1": "game/backtemplo/plx-1.png",
    "layer2": "game/backtemplo/plx-2.png",
    "layer3": "game/backtemplo/plx-3.png",
    "layer4": "game/backtemplo/plx-4.png"
}

# ------------ Fonte ------------
Fonts = {
    "press_start": "game/fonts/PressStart2P.ttf"
}

# ------------ Game Settings ------------


# Sprites dos Inimigos
Enemy_Sprites = {
    "duende": {
        "walk": [f"game/sprites/enemies/duende/walk_frames/walk-{i}.png" for i in range(1, 9)]
    },
    "cogumelo": {
        "walk": [f"game/sprites/enemies/cogumelo/walk_frames/walk-{i}.png" for i in range(1, 9)]
    },
   
    "goblin": {
        "walk": [f"game/sprites/enemies/goblin/walk_frames/walk-{i}.png" for i in range(1, 3)]
    },

    "bat":{
        "walk": [f"game/sprites/enemies/bat_frames/bat_{i}.png" for i in range(1, 6)]
    },

    "blue_monster":{
        "walk": [f"game/sprites/enemies/blue_monster_frames/blue_monster_{i}.png" for i in range(1, 9)]
    },

    "brain":{
        "walk": [f"game/sprites/enemies/brain_frames/brain_{i}.png" for i in range(1, 5)]
    },

    "cacodaemon":{
        "walk": [f"game/sprites/enemies/cacodaemon_frames/cacodaemon_{i}.png" for i in range(1, 7)]
    },

    "ghoul":{
        "walk": [f"game/sprites/enemies/ghoul_frames/ghoul_{i}.png" for i in range(1, 9)]
    },

    "goblin_king":{
        "walk": [f"game/sprites/enemies/goblin_king_frames/goblin_king_{i}.png" for i in range(1, 7)]
    },

    "minotaur":{
        "walk": [f"game/sprites/enemies/minotaur_frames/minotaur_{i}.png" for i in range(1, 9)]
    },

    "snake":{
        "walk": [f"game/sprites/enemies/snake_frames/snake_{i}.png" for i in range(1, 9)]
    },

    "olho":{
        "walk": [f"game/sprites/enemies/olho-voador/fly_frames/fly-{i}.png" for i in range(1, 9)]
    },



} 