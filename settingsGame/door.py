import pygame
from settingsGame.settings_game import Items




class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
       
        # Carrega as imagens da porta
        self.closed_image = pygame.image.load(Items["door_closed"]).convert_alpha()
        self.open_image = pygame.image.load(Items["door_open"]).convert_alpha()
       
        # Ajusta o tamanho (similar ao Exit do código de referência)
        target_width = 50
        target_height = int(50 * 1.5)  # Similar ao Exit que usa tile_size * 1.5
        
        self.closed_image = pygame.transform.scale(self.closed_image, (target_width, target_height))
        self.open_image = pygame.transform.scale(self.open_image, (target_width, target_height))
       
        # Configura a imagem inicial (fechada)
        self.image = self.closed_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height + 50
       
        # Estado da porta
        self.is_open = False
   
    def open(self):
        """Abre a porta"""
        if not self.is_open:
            self.is_open = True
            self.image = self.open_image
   
    def update(self):
        """Atualiza a porta"""
        if self.is_open:
            self.image = self.open_image
        else:
            self.image = self.closed_image
