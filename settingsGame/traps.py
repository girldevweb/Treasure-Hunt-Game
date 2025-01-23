import pygame
from settingsGame.settings_game import Items

class Trap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_time = 0
        self.animation_speed = 0.1
        self.frame_index = 0
        self.damage = 1  # Dano padrão


class Lava(Trap):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(Items["lava"]).convert_alpha()
        self.frame_width = self.spritesheet.get_width()  # 1 frame
        self.frame_height = self.spritesheet.get_height()
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = 1
        
    def load_frames(self):
        frames = []
        for i in range(1):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames
        
    def update(self, dt):
        """Atualiza a animação da lava"""
        self.animation_time += dt
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

class Fire(Trap):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(Items["fire"]).convert_alpha()
        self.frame_width = self.spritesheet.get_width() // 4  # 4 frames
        self.frame_height = self.spritesheet.get_height()
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.damage = 1  # Fogo causa mais dano
        
    def load_frames(self):
        frames = []
        for i in range(4):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

class Spike(Trap):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(Items["spike"]).convert_alpha()
        self.frame_width = self.spritesheet.get_width()  # 1 frame
        self.frame_height = self.spritesheet.get_height()
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_active = False
        self.activation_timer = 0
        self.activation_delay = 2  # Tempo em segundos entre ativações
        
    def load_frames(self):
        frames = []
        for i in range(1):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames
    
    def update(self, dt):
        """Atualiza o estado da armadilha"""
        pass

class Suriken(Trap):
    def __init__(self, x, y, move_distance=40, speed=1):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(Items["suriken"]).convert_alpha()
        self.frame_width = self.spritesheet.get_width() // 8  # 8 frames
        self.frame_height = self.spritesheet.get_height()
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_x = x
        self.move_distance = move_distance
        self.speed = speed
        self.direction = 1
        self.visible_height = 0  # Altura visível inicial
        self.max_height = self.frame_height//2
        self.emerge_speed = 2  # Velocidade de surgimento
        self.is_emerging = True
        self.has_emerged = False
        
    def load_frames(self):
        frames = []
        for i in range(8):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames
    

    def update(self, dt):
        """Atualiza a animação e movimento da armadilha"""
        # Atualiza a animação de rotação
        self.animation_time += dt
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
        
        # Movimento horizontal
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.original_x) > self.move_distance:
            self.direction *= -1


            
def update_traps(traps_group, dt):
    """Atualiza todas as armadilhas"""
    for trap in traps_group:
        trap.update(dt) 
        # Atualiza animação
        trap.animation_time += dt
        if trap.animation_time >= trap.animation_speed:
            trap.animation_time = 0
            trap.frame_index = (trap.frame_index + 1) % len(trap.frames)
            trap.image = trap.frames[trap.frame_index]
        
        # Atualiza comportamento específico
        if isinstance(trap, Suriken):
            # Movimento horizontal da suriken
            trap.rect.x += trap.speed * trap.direction
            if abs(trap.rect.x - trap.original_x) > trap.move_distance:
                trap.direction *= -1
        
        elif isinstance(trap, Spike):
            # Atualiza timer de ativação
            trap.activation_timer += dt
            if trap.activation_timer >= trap.activation_delay:
                trap.activation_timer = 0
                trap.is_active = not trap.is_active
                trap.frame_index = len(trap.frames) - 1 if trap.is_active else 0
                trap.image = trap.frames[trap.frame_index]

def create_trap(trap_type, x, y, **kwargs):
    """Cria uma armadilha do tipo especificado"""
    trap_classes = {
        'F': Fire,
        'S': Spike,
        'R': Suriken,
        'L': Lava
    }
    
    if trap_type in trap_classes:
        return trap_classes[trap_type](x, y, **kwargs)
    return None

