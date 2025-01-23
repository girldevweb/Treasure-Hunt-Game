import pygame
from settingsGame.settings_game import Items

class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carrega as imagens do baú
        self.locked_image = pygame.image.load(Items["bau_locked"]).convert_alpha()
        self.open_image = pygame.image.load(Items["bau_open"]).convert_alpha()
       
        # Começa com o baú trancado
        self.image = self.locked_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       
        self.is_locked = True
        self.is_opened = False  # Novo estado para controlar se já foi aberto
       
    def try_open(self, has_key):
        """Tenta abrir o baú se tiver a chave"""
        if self.is_locked and has_key and not self.is_opened:
            self.is_locked = False
            self.is_opened = True
            self.image = self.open_image
            return True  # Retorna True se conseguiu abrir
        return False  # Retorna False se não conseguiu abrir


