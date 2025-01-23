import pygame
from settingsGame.settings_game import GameSettings, BackCaves, Tiles, world_data2, Player_Sprites, Enemy_Sprites, Items, Sounds
import os
import math
from settingsGame.score import ScoreSystem

from menus.settingsbutton import SettingsMenu
from menus.game_over import GameOver
from settingsGame.door import Door  # Adicione este import no topo
from settingsGame.level_manager import LevelManager
from settingsGame.level_reset_manager import LevelResetManager
from settingsGame.traps import   Spike, create_trap, update_traps

class Level2:
    class SettingsMenu:
        def __init__(self, game):
            self.game = game
            self.screen = game.window.get_screen()
            
            # Dimensões e posição do menu
            self.width = 300
            self.height = 350
            self.x = (GameSettings["WINDOW_WIDTH"] - self.width) // 2
            self.y = (GameSettings["WINDOW_HEIGHT"] - self.height) // 2
            
            # Cores estilo pixel art/retro
            self.bg_color = (48, 44, 46)  # Cinza escuro
            self.border_color = (255, 198, 10)  # Amarelo retro
            self.text_color = (255, 255, 255)  # Branco
            self.button_color = (92, 148, 252)  # Azul retro
            self.button_hover_color = (255, 89, 94)  # Vermelho retro
            self.shadow_color = (32, 30, 32)  # Sombra escura
            
            # Carrega os ícones
            icon_size = (30, 30)
            self.home_img = pygame.transform.scale(
                pygame.image.load(Items["home"]).convert_alpha(), icon_size)
            self.audio_on_img = pygame.transform.scale(
                pygame.image.load(Items["audio_on"]).convert_alpha(), icon_size)
            self.audio_off_img = pygame.transform.scale(
                pygame.image.load(Items["audio_off"]).convert_alpha(), icon_size)
            self.play_img = pygame.transform.scale(
                pygame.image.load(Items["play"]).convert_alpha(), icon_size)
            
            # Configuração dos botões
            button_y_start = self.y + 120
            button_spacing = 70
            
            # Botões com efeito de profundidade
            button_width = 180
            button_height = 50
            center_x = self.x + self.width//2
            
            # Retângulos dos botões (principal e sombra)
            self.home_rect = pygame.Rect(0, 0, button_width, button_height)
            self.home_rect.center = (center_x, button_y_start)
            self.home_shadow = self.home_rect.copy()
            self.home_shadow.y += 4
            
            self.audio_rect = pygame.Rect(0, 0, button_width, button_height)
            self.audio_rect.center = (center_x, button_y_start + button_spacing)
            self.audio_shadow = self.audio_rect.copy()
            self.audio_shadow.y += 4
            
            self.play_rect = pygame.Rect(0, 0, button_width, button_height)
            self.play_rect.center = (center_x, button_y_start + 2 * button_spacing)
            self.play_shadow = self.play_rect.copy()
            self.play_shadow.y += 4
            
            # Sincroniza o estado inicial do áudio com o level
            self.is_audio_on = game.level1.is_sound_on
            
            # Fonte pixel art
            self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
            self.button_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 12)
            
            # Carrega o som de clique
            self.click_sound = pygame.mixer.Sound(os.path.join("game/sounds", "click.wav"))

        def draw_button(self, rect, shadow_rect, icon, text, is_hovered=False):
            # Desenha sombra do botão
            pygame.draw.rect(self.screen, self.shadow_color, shadow_rect, border_radius=8)
            
            # Desenha o botão principal
            button_color = self.button_hover_color if is_hovered else self.button_color
            pygame.draw.rect(self.screen, button_color, rect, border_radius=8)
            
            # Borda pixel art
            border_rects = [
                (rect.left, rect.top, rect.width, 2),  # Top
                (rect.left, rect.bottom-2, rect.width, 2),  # Bottom
                (rect.left, rect.top, 2, rect.height),  # Left
                (rect.right-2, rect.top, 2, rect.height)  # Right
            ]
            for border_rect in border_rects:
                pygame.draw.rect(self.screen, self.border_color, border_rect)
            
            # Desenha o ícone
            icon_x = rect.left + 20
            icon_y = rect.centery - icon.get_height()//2
            self.screen.blit(icon, (icon_x, icon_y))
            
            # Desenha o texto com sombra
            text_surf = self.button_font.render(text, True, self.text_color)
            text_rect = text_surf.get_rect(midleft=(icon_x + icon.get_width() + 10, rect.centery))
            
            # Sombra do texto
            text_shadow = self.button_font.render(text, True, self.shadow_color)
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            self.screen.blit(text_shadow, shadow_rect)
            self.screen.blit(text_surf, text_rect)

        def draw(self):
            # Escurece o fundo do jogo
            dark_surface = pygame.Surface((GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"]))
            dark_surface.fill((0, 0, 0))
            dark_surface.set_alpha(128)
            self.screen.blit(dark_surface, (0, 0))
            
            # Desenha o painel principal com sombra
            pygame.draw.rect(self.screen, self.shadow_color, 
                           (self.x+4, self.y+4, self.width, self.height), border_radius=12)
            pygame.draw.rect(self.screen, self.bg_color, 
                           (self.x, self.y, self.width, self.height), border_radius=12)
            
            # Borda pixel art do painel
            border_rects = [
                (self.x, self.y, self.width, 4),  # Top
                (self.x, self.y+self.height-4, self.width, 4),  # Bottom
                (self.x, self.y, 4, self.height),  # Left
                (self.x+self.width-4, self.y, 4, self.height)  # Right
            ]
            for border_rect in border_rects:
                pygame.draw.rect(self.screen, self.border_color, border_rect)
            
            # Desenha o título com sombra
            title = self.title_font.render("SETTINGS", True, self.text_color)
            title_shadow = self.title_font.render("SETTINGS", True, self.shadow_color)
            
            title_rect = title.get_rect(center=(self.x + self.width//2, self.y + 60))
            shadow_rect = title_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            
            self.screen.blit(title_shadow, shadow_rect)
            self.screen.blit(title, title_rect)
            
            # Verifica hover dos botões
            mouse_pos = pygame.mouse.get_pos()
            home_hover = self.home_rect.collidepoint(mouse_pos)
            audio_hover = self.audio_rect.collidepoint(mouse_pos)
            play_hover = self.play_rect.collidepoint(mouse_pos)
            
            # Desenha os botões
            self.draw_button(self.home_rect, self.home_shadow, self.home_img, "MENU", home_hover)
            self.draw_button(self.audio_rect, self.audio_shadow,
                           self.audio_on_img if self.is_audio_on else self.audio_off_img,
                           "SOUND", audio_hover)
            self.draw_button(self.play_rect, self.play_shadow, self.play_img, "CONTINUE", play_hover)

        def handle_click(self, pos):
            if self.home_rect.collidepoint(pos):
                self.click_sound.play()
                # Para o som do tema antes de sair
                self.game.level2.theme_sound.stop()
                return "home"
            elif self.audio_rect.collidepoint(pos):
                self.click_sound.play()
                self.is_audio_on = not self.is_audio_on
                # Atualiza o estado do som no level
                self.game.level2.is_sound_on = self.is_audio_on
                
                # Ativa/desativa o som do tema do level
                if self.is_audio_on:
                    self.game.level2.theme_sound.play(-1)
                else:
                    self.game.level2.theme_sound.stop()
                return "audio"
            elif self.play_rect.collidepoint(pos):
                self.click_sound.play()
                return "continue"
            return None

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, game):
            super().__init__()
            self.game = game

            # Salva a posição inicial para o reset
            self.initial_x = x
            self.initial_y = y
            self.idle_frames = []
            self.idle_frames_left = []
            self.run_frames = []
            self.run_frames_left = []
            
            # Carrega frames de idle
            for frame in Player_Sprites["idle"]:
                img = pygame.image.load(frame).convert_alpha()
                img = pygame.transform.scale(img, (40, 80))
                self.idle_frames.append(img)
                self.idle_frames_left.append(pygame.transform.flip(img, True, False))
            
            # Carrega frames de corrida
            for frame in Player_Sprites["run"]:
                img = pygame.image.load(frame).convert_alpha()
                img = pygame.transform.scale(img, (40, 80))
                self.run_frames.append(img)
                self.run_frames_left.append(pygame.transform.flip(img, True, False))
            
            # Configuração inicial do player
            self.index = 0
            self.counter = 0
            self.image = self.idle_frames[self.index]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.vel_y = 0
            self.direction = 0
            self.is_running = False
            self.jumps_left = 2  # Número de pulos disponíveis
            self.space_pressed = False
            self.width = 40  # Largura do player
            self.height = 80  # Altura do player
            self.in_air = True
            self.is_dying = False
            self.death_speed = 5
            self.death_rotation = 0
            self.original_image = None
            
            self.is_invulnerable = False
            self.invulnerable_timer = 0
            self.invulnerable_duration = 1.5
            
            # Carrega o som de ataque
            self.attack_sound = pygame.mixer.Sound(Sounds["attack"])
            self.hit_sound = pygame.mixer.Sound(Sounds["hit"])
            
            self.knockback_speed = 8
            self.knockback_duration = 10
            self.knockback_timer = 0
            self.is_knockback = False
            
            # Atributos do escudo
            self.has_shield = False
            self.shield_timer = 0
            self.shield_duration = 10
            self.shield_active = False
            self.shield_pulse = 0  # Para efeito pulsante
            self.shield_pulse_speed = 4  # Velocidade da pulsação
            self.shield_base_size = 6  # Tamanho base do brilho
            
            # Carrega o som de pulo
            self.jump_sound = pygame.mixer.Sound(Sounds["jump"])

        def check_collision(self, dx, dy):
            for tile in self.game.tile_list:
                # Cria retângulos temporários para teste de colisão
                next_x = pygame.Rect(self.rect.x + dx, self.rect.y, self.width, self.height)
                next_y = pygame.Rect(self.rect.x, self.rect.y + dy, self.width, self.height)
                
                # Colisão em X
                if tile[1].colliderect(next_x):
                    dx = 0
                
                # Colisão em Y
                if tile[1].colliderect(next_y):
                    # Colisão com o teto
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Colisão com o chão
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        self.jumps_left = 2
            
            return dx, dy

        def apply_knockback(self, enemy_pos):
            # Determina a direção do knockback baseado na posição relativa do inimigo
            if self.rect.centerx < enemy_pos[0]:
                self.knockback_direction = -1  # Knockback para esquerda
            else:
                self.knockback_direction = 1   # Knockback para direita
            
            self.is_knockback = True
            self.knockback_timer = self.knockback_duration
            self.vel_y = -8  # Pequeno pulo ao tomar dano

        def check_enemy_collision(self):
            # Se estiver em knockback, não pode atacar
            if self.is_knockback:
                return False
                
            # Se estiver invulnerável, não pode tomar dano
            if self.is_invulnerable:
                return False

            for enemy in self.game.enemy_group:
                if enemy.is_dying:
                    continue
                
                if self.rect.colliderect(enemy.rect):
                    # Se tiver escudo ativo, mata o inimigo
                    if self.shield_active:
                        self.game.audio_manager.play_effect("attack")
                        enemy.die()
                        return True
                        
                    # Verifica se o player está caindo e acima do inimigo
                    if self.vel_y > 0 and self.rect.bottom < enemy.rect.centery:
                        # Só pode atacar se não estiver em knockback
                        if not self.is_knockback:
                            self.attack_sound.play()
                            self.vel_y = -15
                            enemy.die()
                            return True
                    else:
                        # Só toma dano se não estiver em knockback ou invulnerável
                        if not self.is_knockback and not self.is_invulnerable:
                            self.game.player_health -= 1
                            if self.game.player_health <= 0:
                                self.game.show_game_over = True
                                self.game.game_over_screen = GameOver(self.game, self.game.score_system.score)
                                self.game.is_paused = True
                            self.is_invulnerable = True
                            self.hit_sound.play()
                            self.apply_knockback((enemy.rect.centerx, enemy.rect.centery))
                            return False
            return False

        def update(self, keyboard):
            # Atualiza o timer de invencibilidade
            if self.is_invulnerable:
                self.invulnerable_timer += 1/60
                if self.invulnerable_timer >= self.invulnerable_duration:
                    self.is_invulnerable = False
                    self.invulnerable_timer = 0

            # Atualiza o timer do escudo
            if self.shield_active:
                self.shield_timer += 1/60  # Assumindo 60 FPS
                if self.shield_timer >= self.shield_duration:
                    self.shield_active = False
                    self.has_shield = False
                    self.shield_timer = 0

            dx = 0
            dy = 0
            walk_cooldown = 5
            
            # Reset estado de corrida no início de cada frame
            self.is_running = False
            
            # Aplica knockback se ativo
            if self.is_knockback:
                dx = self.knockback_speed * self.knockback_direction
                self.knockback_timer -= 1
                if self.knockback_timer <= 0:
                    self.is_knockback = False
            else:
                # Movimento normal do player (apenas se não estiver em knockback)
                if keyboard.key_pressed("LEFT"):
                    dx -= 5
                    self.counter += 1
                    self.direction = -1
                    self.is_running = True
                if keyboard.key_pressed("RIGHT"):
                    dx += 5
                    self.counter += 1
                    self.direction = 0
                    self.is_running = True
            
            # Sistema de pulo duplo
            if keyboard.key_pressed("UP"):
                if not self.space_pressed and self.jumps_left > 0:
                    self.vel_y = -15
                    self.jumps_left -= 1
                    self.in_air = True
                    self.game.audio_manager.play_effect("jump")
                self.space_pressed = True
            else:
                self.space_pressed = False
            
            # Animação
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                
                if self.is_running:
                    # Animação de corrida
                    if self.index >= len(self.run_frames):
                        self.index = 0
                    if self.direction == 0:
                        self.image = self.run_frames[self.index]
                    else:
                        self.image = self.run_frames_left[self.index]
                else:
                    # Animação idle (parado)
                    if self.index >= len(self.idle_frames):
                        self.index = 0
                    if self.direction == 0:
                        self.image = self.idle_frames[self.index]
                    else:
                        self.image = self.idle_frames_left[self.index]

            # Incrementa o contador mesmo quando parado para manter a animação idle
            self.counter += 1

            # Gravidade
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Verifica colisões e atualiza posição
            dx, dy = self.check_collision(dx, dy)
            
            # Atualiza posição
            self.rect.x += dx
            self.rect.y += dy

            # Colisão com o chão do mundo
            if self.rect.bottom > self.game.world_height:
                self.rect.bottom = self.game.world_height
                self.vel_y = 0
                self.in_air = False
                self.jumps_left = 2

            # Verifica colisões com inimigos após atualizar posição
            self.check_enemy_collision()

        def activate_shield(self):
            self.has_shield = True
            self.shield_timer = 0
            self.shield_active = True

        def reset_position(self):
            """Reinicia a posição do jogador"""
            self.rect.x = self.initial_x
            self.rect.y = self.initial_y
            self.vel_y = 0
            self.in_air = True
            self.jumps_left = 2
            self.shield_active = False

        def take_damage(self, damage=1):
          """Aplica dano ao player quando colide com inimigos ou boss"""
          if not self.is_invulnerable:
              self.game.player_health -= damage
              self.is_invulnerable = True
              self.invulnerable_timer = 0
              self.hit_sound.play()
              
              if self.game.player_health <= 0:
                  self.game.show_game_over = True
                  self.game.game_over_screen = GameOver(self.game, self.game.score_system.score)
                  self.game.is_paused = True

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, enemy_type, game):
            super().__init__()
            self.game = game
            self.enemy_type = enemy_type
            self.walk_frames = []
            self.walk_frames_left = []
            
            # Tamanhos específicos para cada tipo de inimigo
            enemy_sizes = {
                "duende": (60, 60),
                "cogumelo": (55, 55),
                "goblin": (55, 55),
                "goblin_king": (60, 60),
                "minotaur": (60, 60),
                "snake": (85, 85),
                "brain": (55, 55),
                "cacodaemon": (60, 60),
                "ghoul": (55, 55),
                "bat": (55, 55),
                "blue_monster": (60, 60),
                "olho": (55, 55)
            }
            
            # Pega o tamanho específico do inimigo ou usa um tamanho padrão
            self.size = enemy_sizes.get(enemy_type, (60, 60))
            
            # Carrega frames de caminhada com o novo tamanho
            for frame in Enemy_Sprites[enemy_type]["walk"]:
                img = pygame.image.load(frame).convert_alpha()
                img = pygame.transform.scale(img, self.size)  # Usa o novo tamanho
                self.walk_frames.append(img)
                self.walk_frames_left.append(pygame.transform.flip(img, True, False))
            
            self.image = self.walk_frames[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - (self.size[1] - 40)  # Ajusta posição Y para compensar o novo tamanho
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            
            self.move_direction = 1
            self.move_counter = 0
            self.frame_index = 0
            self.animation_speed = 0.15
            self.animation_time = 0
            self.vel_y = 0
            self.check_ahead = True  # Flag para verificar à frente
            self.is_dying = False
            self.death_speed = 5
            self.death_rotation = 0
            self.original_image = None
            
        def check_platform_edges(self):
            # Verifica se há chão à frente
            if self.move_direction > 0:  # Movendo para direita
                # Ponto de verificação à frente e abaixo
                ahead_x = self.rect.right + 5
                test_point = (ahead_x, self.rect.bottom + 5)
            else:  # Movendo para esquerda
                # Ponto de verificação à frente e abaixo
                ahead_x = self.rect.left - 5
                test_point = (ahead_x, self.rect.bottom + 5)
            
            # Verifica se há algum tile nesse ponto
            platform_ahead = False
            for tile in self.game.tile_list:
                # Se encontrar um tile na mesma altura
                if (tile[1].top <= self.rect.bottom <= tile[1].bottom + 5 and
                    tile[1].left <= ahead_x <= tile[1].right):
                    platform_ahead = True
                    break
            
            # Se não houver plataforma à frente, muda direção
            if not platform_ahead and self.check_ahead:
                self.move_direction *= -1

        def check_collision(self, dx, dy):
            for tile in self.game.tile_list:
                # Colisão em X
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.move_direction *= -1
                    dx = 0
                
                # Colisão em Y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y >= 0:  # Caindo
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.check_ahead = True  # Ativa verificação quando está no chão
                    elif self.vel_y < 0:  # Subindo
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                        self.check_ahead = False  # Desativa verificação quando está no ar
            
            return dx, dy
        
        def die(self):
            if not self.is_dying:
                self.is_dying = True
                self.vel_y = -15
                # Adiciona pontos quando o inimigo morre
                self.game.score_system.add_points(self.enemy_type)
        
        def update(self):
            if self.is_dying:
                # Apenas cai para fora da tela
                self.vel_y += 0.8
                self.rect.y += self.vel_y
                
                # Remove o inimigo quando sair da tela
                if self.rect.top > self.game.world_height:
                    self.kill()
                return
            
            dx = self.move_direction * 2
            dy = 0
            
            # Gravidade
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            
            # Verifica borda da plataforma
            self.check_platform_edges()
            
            # Verifica colisões
            dx, dy = self.check_collision(dx, dy)
            
            # Atualiza posição
            self.rect.x += dx
            self.rect.y += dy
            
            # Animação
            self.animation_time += self.animation_speed
            if self.animation_time >= 1:
                self.animation_time = 0
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                
                if self.move_direction > 0:
                    self.image = self.walk_frames[self.frame_index]
                else:
                    self.image = self.walk_frames_left[self.frame_index]

    class HealthBar(pygame.sprite.Sprite):
        def __init__(self, x, y, game):
            super().__init__()
            self.game = game
            self.hearts = []
            self.max_health = 3
            self.current_health = 3
            
            # Carrega a spritesheet dos corações
            heart_sheet = pygame.image.load(Items["heart"]).convert_alpha()
            
            # Dimensões de cada frame na spritesheet
            frame_width = heart_sheet.get_width() // 6  # 6 frames na horizontal
            frame_height = heart_sheet.get_height()
            
            # Tamanho para exibição
            display_width = 25
            display_height = 25
            
            # Extrai todos os frames da spritesheet
            self.heart_frames = []
            for i in range(6):  # 6 frames de animação
                frame = heart_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (display_width, display_height))
                self.heart_frames.append(frame)
            
            # Posiciona os corações lado a lado
            for i in range(self.max_health):
                heart = {
                    'frame_index': 0,
                    'animation_time': 0,
                    'rect': pygame.Rect(x + (i * (display_width + 3)), y, display_width, display_height)
                }
                self.hearts.append(heart)

        def update_health(self, health):
            self.current_health = max(0, min(health, self.max_health))

        def update(self, dt):
            # Atualiza a animação de cada coração
            for heart in self.hearts:
                heart['animation_time'] += dt
                if heart['animation_time'] >= 0.1:  # Velocidade da animação
                    heart['animation_time'] = 0
                    heart['frame_index'] = (heart['frame_index'] + 1) % len(self.heart_frames)

        def draw(self, screen):
            # Desenha os corações com animação
            for i, heart in enumerate(self.hearts):
                if i < self.current_health:
                    current_frame = self.heart_frames[heart['frame_index']]
                    screen.blit(current_frame, heart['rect'])

    class SettingsButton(pygame.sprite.Sprite):
        def __init__(self, game):
            super().__init__()
            self.game = game
            
            # Carrega a spritesheet do botão
            settings_sheet = pygame.image.load(Items["settings"]).convert_alpha()
            
            # Dimensões de cada frame na spritesheet
            frame_width = settings_sheet.get_width() // 3  # 3 frames na horizontal
            frame_height = settings_sheet.get_height()
            
            # Tamanho para exibição
            self.display_width = 30
            self.display_height = 30
            
            # Extrai todos os frames da spritesheet
            self.frames = []
            for i in range(3):  # 3 frames de animação
                frame = settings_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (self.display_width, self.display_height))
                self.frames.append(frame)
            
            # Configuração da animação
            self.frame_index = 0
            self.animation_time = 0
            
            # Posição no canto superior direito
            x = GameSettings["WINDOW_WIDTH"] - self.display_width - 10  # 10 pixels de margem
            y = 20
            self.rect = pygame.Rect(x, y, self.display_width, self.display_height)

        def update(self, dt):
            # Atualiza a animação
            self.animation_time += dt
            if self.animation_time >= 0.2:  # Velocidade da animação
                self.animation_time = 0
                self.frame_index = (self.frame_index + 1) % len(self.frames)

        def draw(self, screen):
            current_frame = self.frames[self.frame_index]
            screen.blit(current_frame, self.rect)

    class CollectiblesDisplay:
        def __init__(self, game):
            self.game = game
            self.screen = game.window.get_screen()
            
            # Tamanho de cada frame nos spritesheets
            self.sprite_size = 32
            self.icon_size = (32, 32)
            
            # Carrega os spritesheets
            self.coin_frames = self.load_spritesheet(Items["coin"], 8)
            self.key_frames = self.load_spritesheet(Items["key"], 8)
            self.potion_frames = self.load_spritesheet(Items["potion"], 8)
            
            # Índices de animação
            self.coin_index = 0
            self.key_index = 0
            self.potion_index = 0
            
            # Contadores de animação
            self.animation_speed = 0.2
            self.coin_counter = 0
            self.key_counter = 0
            self.potion_counter = 0
            
            # Posição inicial (à direita da tela)
            self.spacing = 90  # Aumentado de 80 para 90
            base_y = 20  # Posição Y para todos os ícones
            
            # Calcula as posições dos ícones (da direita para a esquerda)
            settings_x = GameSettings["WINDOW_WIDTH"] - 60  # Aumentado de 40 para 60
            
            # Posições dos ícones
            self.coin_pos = (settings_x - self.spacing * 3, base_y)
            self.key_pos = (settings_x - self.spacing * 2, base_y)
            self.potion_pos = (settings_x - self.spacing, base_y)
            
            # Contadores de itens
            self.coin_count = 0
            self.key_count = 0
            self.potion_count = 0
            
            # Fonte menor para os contadores
            self.font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 16)
            
            # Cores
            self.text_color = (255, 255, 255)
            self.shadow_color = (0, 0, 0)

        def load_spritesheet(self, path, num_frames):
            # Carrega o spritesheet
            sheet = pygame.image.load(path).convert_alpha()
            frames = []
            
            # Extrai cada frame
            for i in range(num_frames):
                frame = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), (i * self.sprite_size, 0, self.sprite_size, self.sprite_size))
                frame = pygame.transform.scale(frame, self.icon_size)
                frames.append(frame)
            
            return frames

        def update_animation(self, dt):
            # Atualiza os contadores de animação
            self.coin_counter += dt
            self.key_counter += dt
            self.potion_counter += dt
            
            # Atualiza os índices de frame
            if self.coin_counter >= self.animation_speed:
                self.coin_index = (self.coin_index + 1) % 8
                self.coin_counter = 0
                
            if self.key_counter >= self.animation_speed:
                self.key_index = (self.key_index + 1) % 8
                self.key_counter = 0
                
            if self.potion_counter >= self.animation_speed:
                self.potion_index = (self.potion_index + 1) % 8
                self.potion_counter = 0

        def draw_counter(self, pos, count, frames, current_frame):
            # Desenha o frame atual da animação
            self.screen.blit(frames[current_frame], pos)
            
            # Prepara o texto do contador com 'x' antes do número
            count_text = f"x{count}"  # Adiciona 'x' antes do número
            
            # Ajusta a posição do texto para ficar mais próximo e alinhado com o ícone
            text_x = pos[0] + 30
            text_y = pos[1] + 8
            
            # Desenha a sombra do texto
            text_shadow = self.font.render(count_text, True, self.shadow_color)
            shadow_pos = (text_x + 1, text_y + 1)
            self.screen.blit(text_shadow, shadow_pos)
            
            # Desenha o texto
            text_surface = self.font.render(count_text, True, self.text_color)
            text_pos = (text_x, text_y)
            self.screen.blit(text_surface, text_pos)

        def draw(self):
            self.draw_counter(self.coin_pos, self.coin_count, self.coin_frames, self.coin_index)
            self.draw_counter(self.key_pos, self.key_count, self.key_frames, self.key_index)
            self.draw_counter(self.potion_pos, self.potion_count, self.potion_frames, self.potion_index)

        def update_counts(self, coins=None, keys=None, potions=None):
            if coins is not None:
                self.coin_count = coins
            if keys is not None:
                self.key_count = keys
            if potions is not None:
                self.potion_count = potions

    class Collectible(pygame.sprite.Sprite):
        def __init__(self, x, y, type, game):
            super().__init__()
            self.game = game
            self.type = type
            self.frames = []
            
            # Configurações de tamanho para cada tipo de coletável
            sizes = {
                "coin": (30, 30),
                "potion": (30, 30),
                "key": (30, 30)
            }
            
            # Carrega a spritesheet apropriada
            spritesheet = pygame.image.load(Items[type]).convert_alpha()
            
            # Dimensões de cada frame na spritesheet
            frame_width = spritesheet.get_width() // 8  # 8 frames por spritesheet
            frame_height = spritesheet.get_height()
            
            # Extrai os frames da spritesheet
            for i in range(8):
                frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                frame = pygame.transform.scale(frame, sizes[type])
                self.frames.append(frame)
            
            self.image = self.frames[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
            self.frame_index = 0
            self.animation_time = 0
            self.animation_speed = 0.2
            
            # Som de coleta
            self.collect_sound = pygame.mixer.Sound(Sounds["collect"])

    def __init__(self, game):
        self.game = game
        self.reset_manager = LevelResetManager(game)
        self.traps_group = pygame.sprite.Group()
        self.screen = game.window.get_screen()
        self.window = game.window
        self.keyboard = game.window.get_keyboard()
        self.tile_size = GameSettings["TILE_SIZE"]
        self.tile_list = []
        
        # Configuração do FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Inicializa o AudioManager
        self.audio_manager = game.audio_manager
        self.audio_manager.set_level(2)

        # Adicione estas duas linhas aqui
        self.show_game_over = False
        self.game_over_screen = None
        
        # Calcula a largura do mundo baseado na matriz world_data2
        self.world_width = len(world_data2[0]) * self.tile_size
        self.world_height = len(world_data2) * self.tile_size
        
        # Agora carrega as camadas do fundo
        self.bg_layers = []
        for i in range(1, 8):  # 7 camadas
            layer = pygame.image.load(BackCaves[f"layer{i}"]).convert_alpha()
            
            # Calcula a escala necessária para cobrir todo o nível
            scale_x = self.world_width / layer.get_width()
            scale_y = GameSettings["WINDOW_HEIGHT"] / layer.get_height()
            
            # Redimensiona a imagem para cobrir todo o nível horizontalmente
            new_width = int(layer.get_width() * scale_x)
            new_height = int(layer.get_height() * scale_y)
            layer = pygame.transform.scale(layer, (new_width, new_height))
            
            self.bg_layers.append(layer)
        
        # Carregando tiles
        self.dirt_img = pygame.image.load(Tiles["dirt2"]).convert_alpha()
        self.grass_img = pygame.image.load(Tiles["grass2"]).convert_alpha()
        
        # Criando o mundo
        self.create_world()
        
        # Criando o player
        self.player = self.Player(100, GameSettings["WINDOW_HEIGHT"] - 130, self)
        
        # Configuração da câmera
        self.camera_x = 0
        self.camera_y = 0
        self.true_scroll = [0, 0]
        
        self.enemy_group = pygame.sprite.Group()
        self.create_enemies()
        
        # Adiciona barra de vida
        self.health_bar = self.HealthBar(20, 20, self)
        self.player_health = 3
        
        self.settings_button = self.SettingsButton(self)
        self.collectibles_display = self.CollectiblesDisplay(self)
        
        # Adiciona contadores de coletáveis
        self.coins = 0
        self.keys = 0
        self.potions = 0
        
        self.settings_menu = None
        self.show_settings = False
        self.is_paused = False  # Nova variável para controle de pausa
        
        # Grupos de sprites para coletáveis
        self.coins_group = pygame.sprite.Group()
        self.potions_group = pygame.sprite.Group()
        self.keys_group = pygame.sprite.Group()
        
        # Cria os coletáveis
        self.create_collectibles()
        
        # Configuração do som do tema
        self.theme_sound = pygame.mixer.Sound(Sounds["theme2"])
        self.theme_sound.set_volume(0.3)
        self.is_sound_on = True
        
        # Adiciona o sistema de pontuação
        self.score_system = ScoreSystem(self.window)

        self.show_game_over = False
        self.game_over_screen = None
        self.hearts = 3  # Inicializa as vidas do jogador

        # Adicione o grupo de sprites para as portas
        self.doors_group = pygame.sprite.Group()
        
        # No loop que cria o mundo, adicione:
        for y, row in enumerate(world_data2):
            for x, tile in enumerate(row):
                if tile == "D":
                    door = Door(x * self.tile_size, y * self.tile_size)
                    self.doors_group.add(door)

        self.level_manager = LevelManager(game)
        self.current_level = 1  # Indica que é o level 1

    def create_world(self):
        row_count = 0
        for row in world_data2:
            col_count = 0
            for tile in row:
                x = col_count * self.tile_size
                y = row_count * self.tile_size
                if tile == 1:
                    img = pygame.transform.scale(self.dirt_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 2:
                    img = pygame.transform.scale(self.grass_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.tile_size
                    img_rect.y = row_count * self.tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 'F': #adiciona o trap de fogo
                    trap = create_trap('F',  x, y + self.tile_size/2)

                    self.traps_group.add(trap)
                elif tile == 'S': #spike
                  trap = create_trap('S',  x, y + 32)
                  self.traps_group.add(trap)
                elif tile == 'R': # R = Suriken (Estrela ninja)
                  trap = create_trap('R',  x, y + self.tile_size - 16)
                  self.traps_group.add(trap)

                elif tile == 'L': # L = Lava (Lava)
                  trap = create_trap('L',  x, y + 20)
                  self.traps_group.add(trap)
                col_count += 1
            row_count += 1
    
    def update_camera(self):
        # Define o ponto alvo da câmera (centro do player)
        target_x = self.player.rect.centerx - GameSettings["WINDOW_WIDTH"] // 2
        target_y = self.player.rect.centery - GameSettings["WINDOW_HEIGHT"] // 2
        
        # Suaviza o movimento da câmera
        self.true_scroll[0] += (target_x - self.true_scroll[0]) * 0.05
        self.true_scroll[1] += (target_y - self.true_scroll[1]) * 0.05
        
        # Limita a câmera aos limites do mundo
        self.true_scroll[0] = max(0, min(self.true_scroll[0], 
            self.world_width - GameSettings["WINDOW_WIDTH"]))
        self.true_scroll[1] = max(0, min(self.true_scroll[1], 
            self.world_height - GameSettings["WINDOW_HEIGHT"]))
        
        # Converte para inteiros para evitar tremulação
        self.camera_x = int(self.true_scroll[0])
        self.camera_y = int(self.true_scroll[1])

    def draw_background(self):
        # Desenha o fundo com parallax
        for i, layer in enumerate(self.bg_layers):
            # Ajusta o fator de parallax (menor para camadas mais distantes)
            parallax = i * 0.2  # Você pode ajustar este valor
            
            # Calcula a posição X com base no parallax, sem usar módulo
            x = -self.camera_x * parallax
            
            # Desenha a camada
            self.screen.blit(layer, (x, 0))

    def draw_tiles(self):
        for tile in self.tile_list:
            # Desenha apenas os tiles visíveis na tela
            screen_x = tile[1].x - self.camera_x
            screen_y = tile[1].y - self.camera_y
            
            # Verifica se o tile está visível na tela
            if (-tile[1].width <= screen_x <= GameSettings["WINDOW_WIDTH"] and
                -tile[1].height <= screen_y <= GameSettings["WINDOW_HEIGHT"]):
                self.screen.blit(tile[0], (screen_x, screen_y))
               
    
    def draw_grid(self):
        # Função auxiliar para debug - desenha grade
        for line in range(0, 20):
            pygame.draw.line(self.screen, (255, 255, 255), 
                           (0, line * self.tile_size), 
                           (GameSettings["WINDOW_WIDTH"], line * self.tile_size))
            pygame.draw.line(self.screen, (255, 255, 255), 
                           (line * self.tile_size, 0), 
                           (line * self.tile_size, GameSettings["WINDOW_HEIGHT"]))
    
    def update(self):
        # Atualiza o level (pode ser expandido posteriormente)
        pass
    

    def draw_traps(self):
      """Desenha as armadilhas após os tiles"""
      for trap in self.traps_group:
          screen_x = trap.rect.x - self.camera_x
          screen_y = trap.rect.y - self.camera_y
          if (-trap.rect.width <= screen_x <= GameSettings["WINDOW_WIDTH"] and
              -trap.rect.height <= screen_y <= GameSettings["WINDOW_HEIGHT"]):
              self.screen.blit(trap.image, (screen_x, screen_y))


    def draw(self, show_grid=False):
        # Desenha todos os elementos do level
        self.draw_background()
        self.draw_traps()
        self.draw_tiles()
        
        # Desenha os coletáveis
        for group in [self.coins_group, self.potions_group, self.keys_group]:
            for item in group:
                screen_x = item.rect.x - self.camera_x
                screen_y = item.rect.y - self.camera_y
                if (-item.rect.width <= screen_x <= GameSettings["WINDOW_WIDTH"] and
                    -item.rect.height <= screen_y <= GameSettings["WINDOW_HEIGHT"]):
                    self.screen.blit(item.image, (screen_x, screen_y))

         # Desenha as portas (adicione este bloco)
        for door in self.doors_group:
            screen_x = door.rect.x - self.camera_x
            screen_y = door.rect.y - self.camera_y
            if (-door.rect.width <= screen_x <= GameSettings["WINDOW_WIDTH"] and
                -door.rect.height <= screen_y <= GameSettings["WINDOW_HEIGHT"]):
                self.screen.blit(door.image, (screen_x, screen_y))

         # Atualiza o fade do player e efeito de teletransporte antes de desenhar
        #if self.level_manager.player_fading:
            #self.level_manager.update_player_fade(
                #self.player,
                #self.screen,
                #self.camera_x,
                #self.camera_y
           # )

        
        if show_grid:
            self.draw_grid()
    
    def create_enemies(self):
        # Cria inimigos baseado na matriz do mundo
        for y, row in enumerate(world_data2):
            for x, tile in enumerate(row):
                if tile == 3:  # Duende
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "duende", self)
                    self.enemy_group.add(enemy)
                elif tile == 4:  # Cogumelo
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "cogumelo", self)
                    self.enemy_group.add(enemy)
                elif tile == 5:  # Goblin
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "goblin", self)
                    self.enemy_group.add(enemy)

                elif tile == 10:  # Goblin King
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "goblin_king", self)
                    self.enemy_group.add(enemy)

                elif tile == 11:  # Minotaur
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "minotaur", self)
                    self.enemy_group.add(enemy)

                elif tile == 12:  # Sneak
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "snake", self)
                    self.enemy_group.add(enemy)

                elif tile == 13:  # Brain
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "brain", self)
                    self.enemy_group.add(enemy) 

                elif tile == 14:  # Cacodaemon
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "cacodaemon", self)
                    self.enemy_group.add(enemy) 

                elif tile == 15:  # Ghoul
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "ghoul", self)
                    self.enemy_group.add(enemy)

                elif tile == 16:  # Bat
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "bat", self)
                    self.enemy_group.add(enemy) 
                    
                elif tile == 17:  # Blue Monster
                    enemy = self.Enemy(x * GameSettings["TILE_SIZE"], 
                                     y * GameSettings["TILE_SIZE"], 
                                     "blue_monster", self)
                    self.enemy_group.add(enemy) 

    def create_collectibles(self):
        for y, row in enumerate(world_data2):
            for x, tile in enumerate(row):
                if tile == 9:  # Moeda
                    collectible = self.Collectible(x * self.tile_size, y * self.tile_size, "coin", self)
                    self.coins_group.add(collectible)
                elif tile == 7:  # Poção
                    collectible = self.Collectible(x * self.tile_size, y * self.tile_size, "potion", self)
                    self.potions_group.add(collectible)
                elif tile == 8:  # Chave
                    collectible = self.Collectible(x * self.tile_size, y * self.tile_size, "key", self)
                    self.keys_group.add(collectible)

    def check_collectibles(self):
        # Verifica colisão com moedas
        for coin in self.coins_group:
            if self.player.rect.colliderect(coin.rect):
                self.audio_manager.play_effect("collect")
                self.coins += 1
                self.collectibles_display.update_counts(coins=self.coins)
                self.score_system.add_coin()
                coin.kill()
        
        # Verifica colisão com poções
        for potion in self.potions_group:
            if self.player.rect.colliderect(potion.rect):
                self.audio_manager.play_effect("collect")
                self.potions += 1
                self.collectibles_display.update_counts(potions=self.potions)
                self.player.activate_shield()
                potion.kill()
        
        # Verifica colisão com chaves
        for key in self.keys_group:
            if self.player.rect.colliderect(key.rect):
                self.audio_manager.play_effect("collect")
                self.keys += 1
                self.collectibles_display.update_counts(keys=self.keys)
                key.kill()

    def check_door_collision(self):
        """Verifica colisão com a porta usando a mesma lógica do player com tiles"""
        for door in self.doors_group:
            # Verifica colisão em X (como no código de referência)
            if door.rect.colliderect(self.player.rect.x, self.player.rect.y, self.player.width, self.player.height):
                # Verifica se o player está realmente tocando a porta
                if door.rect.colliderect(self.player.rect):
                    if self.keys > 0 and not door.is_open:
                        door.open()
                        self.keys -= 1
                        self.collectibles_display.update_counts(keys=self.keys)
                        result = self.level_manager.check_level_completion(self.player, door, self.score_system.score)
                        if result:
                            return result


    def check_trap_collision(self):
                """Verifica colisão com armadilhas"""

                if not self.player.is_invulnerable and not self.player.shield_active:
                      for trap in self.traps_group:
                          if self.player.rect.colliderect(trap.rect):
                              if isinstance(trap, (Spike)):
                                  if trap.is_active:
                                      self.player.take_damage(trap.damage)
                                      break
                              else:
                                  self.player.take_damage(trap.damage)
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        if not self.audio_manager.is_muted:
            self.audio_manager.play_music("theme2")
        
        while running:
            dt = clock.tick(60) / 1000.0
            update_traps(self.traps_group, dt)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                
                

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                   



                  
                    if self.show_settings:
                        action = self.settings_menu.handle_click()
                        if action == "home":
                            self.audio_manager.stop_music()
                            return "menu"
                        elif action == "continue":
                            self.show_settings = False
                            self.is_paused = False  # Despausa o jogo
                        elif action == "audio":
                            pass
                    elif self.settings_button.rect.collidepoint(event.pos):
                        if not self.show_settings:
                            self.settings_menu = SettingsMenu(self.game)
                            self.show_settings = True
                            self.is_paused = True  # Pausa o jogo
                
                    elif not self.is_paused and not self.show_game_over:
                        if self.player.rect.collidepoint(mouse_pos):
                            self.player.jump()
                            if not self.audio_manager.is_muted:
                                self.audio_manager.play_effect("jump")

               
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.show_settings:
                            self.settings_menu = SettingsMenu(self.game)
                            self.show_settings = True
                            self.is_paused = True
                       
            if self.keyboard.key_pressed("ESC"):
                self.audio_manager.stop_music()
                self.game.current_state = self.game.LEVEL_SELECT
                return
           
            # Limpa a tela
            self.window.set_background_color((0, 0, 0))
           
            # Atualiza e desenha o jogo normalmente
            self.update_camera()
            self.draw()
           
         
            if self.player_health <= 0 and not self.show_game_over:
                self.show_game_over = True
                self.game_over_screen = GameOver(self.game, self.score_system.score)
            
           
           
            # Atualiza apenas se não estiver pausado e não estiver em game over
            if not self.is_paused and not self.show_game_over:
                
        
                self.player.update(self.keyboard)
                self.enemy_group.update()
                self.doors_group.update()
                self.check_door_collision()
                self.check_trap_collision()
                 
            # # Verifica a porta e sua abertura
                for door in self.doors_group:
                    if self.keys > 0 and not door.is_open:
                        distance = math.sqrt(
                            (self.player.rect.centerx - door.rect.centerx) ** 2 +
                            (self.player.rect.centery - door.rect.centery) ** 2
                        )
                        if distance < 100:
                            door.is_open = True
                            self.keys -= 1
                            break  # Sai do loop após abrir uma porta
                
                # Depois verifica se completou o nível
                for door in self.doors_group:
                    if door.is_open:
                        result = self.level_manager.check_level_completion(self.player, door, self.score_system.score)
                        if result:
                            if result == "next":
                                self.audio_manager.stop_music()
                                self.game.level_select.unlock_next_level(2)
                                return "level3"
                            elif result == "restart":
                                self.reset_manager.reset_level(self)
                                self.level_manager.reset()
                            elif result == "home":
                                self.audio_manager.stop_music()
                                return "menu"
                            break  # Sai do loop 
             
               
                # Atualiza animações dos coletáveis
                for group in [self.coins_group, self.potions_group, self.keys_group]:
                    for item in group:
                        item.animation_time += dt
                        if item.animation_time >= item.animation_speed:
                            item.animation_time = 0
                            item.frame_index = (item.frame_index + 1) % len(item.frames)
                            item.image = item.frames[item.frame_index]
               
                # Verifica coleta de itens
                self.check_collectibles()
                self.check_door_collision()
           
            # Desenha os coletáveis
            for group in [self.coins_group, self.potions_group, self.keys_group]:
                for item in group:
                    screen_x = item.rect.x - self.camera_x
                    screen_y = item.rect.y - self.camera_y
                    self.screen.blit(item.image, (screen_x, screen_y))
           
            # Desenha os inimigos
            for enemy in self.enemy_group:
                screen_x = enemy.rect.x - self.camera_x
                screen_y = enemy.rect.y - self.camera_y
                self.screen.blit(enemy.image, (screen_x, screen_y))
           
            # Desenha o escudo (se ativo) e o player
            screen_x = self.player.rect.x - self.camera_x
            screen_y = self.player.rect.y - self.camera_y
           
            if self.player.shield_active:
                # Atualiza o efeito pulsante
                self.player.shield_pulse += self.player.shield_pulse_speed
                pulse = abs(math.sin(self.player.shield_pulse / 30)) * 4
               
                shield_size = self.player.shield_base_size + pulse
               
                # Calcula o centro do player
                center_x = screen_x + self.player.rect.width // 2
                center_y = screen_y + self.player.rect.height // 2
               
                # Raios reduzidos para cada camada do escudo
                base_radius = max(self.player.rect.width, self.player.rect.height) // 2
                outer_radius = base_radius + shield_size + 8
                inner_radius = base_radius + shield_size + 4
                border_radius = base_radius + shield_size + 2
               
                # Escudo externo
                outer_surface = pygame.Surface((outer_radius * 2, outer_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(outer_surface, (100, 200, 255, 40),
                                (outer_radius, outer_radius), outer_radius)
               
                # Escudo interno
                inner_surface = pygame.Surface((inner_radius * 2, inner_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(inner_surface, (0, 150, 255, 100),
                                (inner_radius, inner_radius), inner_radius)
               
                # Borda brilhante
                border_surface = pygame.Surface((border_radius * 2, border_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(border_surface, (150, 230, 255, 160),
                                (border_radius, border_radius), border_radius, 2)
               
                # Desenha as camadas do escudo
                self.screen.blit(outer_surface,
                               (center_x - outer_radius,
                                center_y - outer_radius))
                self.screen.blit(inner_surface,
                               (center_x - inner_radius,
                                center_y - inner_radius))
                self.screen.blit(border_surface,
                               (center_x - border_radius,
                                center_y - border_radius))
           
            # Desenha o player #editei para 
            if self.level_manager.player_visible:
                screen_x = self.player.rect.x - self.camera_x
                screen_y = self.player.rect.y - self.camera_y
                self.screen.blit(self.player.image, (screen_x, screen_y))
           
            self.health_bar.update(dt)
            self.health_bar.update_health(self.player_health)
            self.health_bar.draw(self.screen)
           
            self.settings_button.update(dt)
            self.settings_button.draw(self.screen)
           
            # Atualiza a animação dos coletáveis
            self.collectibles_display.update_animation(dt)
           
            # Atualiza e desenha os coletáveis
            self.collectibles_display.update_counts(
                coins=self.coins,
                keys=self.keys,
                potions=self.potions
            )
            self.collectibles_display.draw()
            
            self.score_system.draw()
           
            # Desenha o menu de configurações por último se estiver ativo
            if self.show_settings:
                self.settings_menu.draw()


             # Se estiver em game over, desenha a tela e verifica ações
            if self.show_game_over:
                result = self.game_over_screen.draw()
                if result:
                    if result == "restart":
                        self.reset_manager.reset_level(self)
                        self.player_health = 3
                        self.show_game_over = False
                    elif result == "home":
                        self.audio_manager.stop_music()
                        return "menu"
                    
             # Verifica e desenha level completed por último
            if not self.is_paused and not self.show_game_over:
                result = self.level_manager.check_level_completion(self.player, door, self.score_system.score)
                if result:
                    if result == "next":
                        self.audio_manager.stop_music()
                        self.game.level_select.unlock_next_level(self.current_level)
                        return f"level{self.current_level + 1}"
                    elif result == "restart":
                        self.reset_manager.reset_level(self)
                        self.level_manager.show_level_completed = False
                    elif result == "home":
                        self.audio_manager.stop_music()
                        return "menu"
           
           
           
            
           
            self.window.update()



    def cleanup(self):
        """Limpa recursos quando sair do level"""
        self.audio_manager.cleanup()
        self.score_system.reset_score()

    
    

