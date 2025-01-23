import pygame
from settingsGame.settings_game import Final_Boss, Items, GameSettings


class FinalBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__()
        self.level = level
        self.game = level.game
       
        # Carrega os frames de animação
        self.frames = [pygame.image.load(frame).convert_alpha() for frame in Final_Boss["boss"]]
        self.frame_index = 0
        self.animation_time = 0
        self.animation_speed = 0.15
       
        # Configuração inicial
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
       
        # Movimento (similar aos inimigos normais)
        self.move_direction = 1
        self.move_counter = 0
        self.speed = 2
       
        # Estados do boss
        self.state = "moving"
        self.state_timer = 0
        self.prepare_attack_duration = 500
        self.attack_duration = 2000
       
        # Ataque
        self.laser_image = pygame.image.load(Items["laser"]).convert_alpha()
        self.lasers = pygame.sprite.Group()
        self.shoot_delay = 500
        self.last_shot = 0
       
        # Status
        self.health = 5
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1000
       
        # Som
        self.laser_sound = pygame.mixer.Sound("game/sounds/laser.mp3")
        self.hit_sound = pygame.mixer.Sound("game/sounds/hit.mp3")
   
    def check_collision(self, dx):
        # Verifica colisão com tiles usando a tile_list do level
        for tile in self.level.tile_list:
            # Verifica a próxima posição
            next_rect = self.rect.copy()
            next_rect.x += dx
            
            if tile[1].colliderect(next_rect):
                # Debug
                self.move_direction *= -1
                self.state = "preparing_attack"
                self.state_timer = pygame.time.get_ticks()
                return 0
        
        # Se não houver colisão, retorna o movimento original
      # Debug
        return dx
   
    def update(self):
        current_time = pygame.time.get_ticks()
       
        # Atualiza invulnerabilidade
        if self.invulnerable and current_time - self.invulnerable_timer > self.invulnerable_duration:
            self.invulnerable = False
       
        # Máquina de estados do boss
        if self.state == "moving":
            # Move horizontalmente
            dx = self.move_direction * self.speed
            dx = self.check_collision(dx)
            self.rect.x += dx
          
           
        elif self.state == "preparing_attack":
            if current_time - self.state_timer > self.prepare_attack_duration:
                self.state = "attacking"
                self.state_timer = current_time
           
        elif self.state == "attacking":
            if current_time - self.last_shot > self.shoot_delay:
                self.shoot()
                self.last_shot = current_time
           
            if current_time - self.state_timer > self.attack_duration:
                self.state = "moving"
             
       
        # Animação
        self.animation_time += self.animation_speed
        if self.animation_time >= 1:
            self.animation_time = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            if self.move_direction > 0:
                self.image = self.frames[self.frame_index]
            else:
                self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
       
        # Atualiza os lasers
      
      
        self.lasers.update()
    


    def reverse_direction(self):
        """Inverte a direção do movimento do boss"""
        self.move_direction *= -1
        # Atualiza a imagem para a direção correta
        if self.move_direction > 0:
            self.image = self.frames[self.frame_index]
        else:
            self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
            
    def shoot(self):
        """Atira um laser na direção atual"""
        if self.move_direction == 1:  # Atirando para a direita
            laser_x = self.rect.right  # Posição inicial do laser na direita do boss
        else:  # Atirando para a esquerda
            laser_x = self.rect.left  # Posição inicial do laser na esquerda do boss
       
        laser = Laser(laser_x, self.rect.centery, self.laser_image)
        laser.direction = self.move_direction
       
        if self.move_direction == -1:  # Se o boss está olhando para a esquerda
            laser.image = pygame.transform.flip(laser.image, True, False)
            # Ajusta a posição do laser para compensar a mudança de direção
            laser.rect.centerx = self.rect.left
        else:
            laser.rect.centerx = self.rect.right
       
        self.lasers.add(laser)
        self.laser_sound.play()
    def take_damage(self):
      """Recebe dano quando o player pula em cima ou ataca com escudo"""
      if not self.invulnerable:
          self.health -= 1
          self.invulnerable = True
          self.invulnerable_timer = pygame.time.get_ticks()
          self.hit_sound.play()
         
          # Retorna True se o boss foi derrotado
          return self.health <= 0
      return False

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
        self.direction = 1
       
    def update(self):
        self.rect.x += self.speed * self.direction
        # Remove o laser se sair da tela
        if self.rect.right < 0 or self.rect.left > GameSettings["WINDOW_WIDTH"]:
            self.kill()
