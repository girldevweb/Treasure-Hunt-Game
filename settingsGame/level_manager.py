import pygame
from settingsGame.settings_game import Fonts
import math

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.screen = game.window.get_screen()
        self.show_level_completed = False
        self.player_visible = True
        
        # Configurações da janela
        self.width = 400
        self.height = 400
        self.x = (game.window.width - self.width) // 2
        self.y = (game.window.height - self.height) // 2
        
        # Cores atualizadas para combinar com Game Over
        self.window_color = (41, 41, 41)  # Cinza escuro
        self.border_color = (255, 198, 10)  # Dourado
        self.title_color = (255, 198, 10)  # Dourado
        self.score_color = (255, 198, 10)  # Dourado
        self.button_colors = {
            'next': {
                'normal': (70, 70, 70),    # Cinza médio
                'hover': (100, 100, 100)   # Cinza claro
            },
            'restart': {
                'normal': (70, 70, 70),    # Cinza médio
                'hover': (100, 100, 100)   # Cinza claro
            },
            'home': {
                'normal': (70, 70, 70),    # Cinza médio
                'hover': (100, 100, 100)   # Cinza claro
            }
        }
        
        # Botões
        button_width = 200
        button_height = 50
        button_spacing = 30
        start_x = self.x + (self.width - button_width) // 2
        start_y = self.y + 140
        
        self.next_button = pygame.Rect(start_x, start_y, button_width, button_height)
        self.restart_button = pygame.Rect(start_x, start_y + button_height + button_spacing, button_width, button_height)
        self.home_button = pygame.Rect(start_x, start_y + 2 * (button_height + button_spacing), button_width, button_height)
        
        # Fontes com Press Start 2P
        self.font = pygame.font.Font(Fonts["press_start"], 24)        # Título
        self.font_score = pygame.font.Font(Fonts["press_start"], 16)  # Score
        self.font_buttons = pygame.font.Font(Fonts["press_start"], 16) # Botões
        
    def check_level_completion(self, player, door, score):
        if pygame.sprite.collide_rect(player, door) and door.is_open:
            self.show_level_completed = True
            self.player_visible = False
            return self.draw()
        return None
    
    def show_level_completed(self):
        """Loop dedicado para a tela de level completed"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
            
            # Desenha a janela
            pygame.draw.rect(self.screen, (200, 200, 200), 
                           (self.x, self.y, self.width, self.height))
            
            # Título
            title = self.font.render("LEVEL COMPLETED!", True, (0, 0, 0))
            title_rect = title.get_rect(center=(self.x + self.width//2, self.y + 30))
            self.screen.blit(title, title_rect)
            
            # Score
            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(self.x + self.width//2, self.y + 70))
            self.screen.blit(score_text, score_rect)
            
            # Botões
            mouse_pos = pygame.mouse.get_pos()
            
            # Next Button (Verde)
            color = (120, 220, 120) if self.next_button.collidepoint(mouse_pos) else (100, 200, 100)
            pygame.draw.rect(self.screen, color, self.next_button)
            next_text = self.font.render("NEXT", True, (0, 0, 0))
            next_rect = next_text.get_rect(center=self.next_button.center)
            self.screen.blit(next_text, next_rect)
            
            # Restart Button (Vermelho)
            color = (220, 120, 120) if self.restart_button.collidepoint(mouse_pos) else (200, 100, 100)
            pygame.draw.rect(self.screen, color, self.restart_button)
            restart_text = self.font.render("RESTART", True, (0, 0, 0))
            restart_rect = restart_text.get_rect(center=self.restart_button.center)
            self.screen.blit(restart_text, restart_rect)
            
            # Home Button (Azul)
            color = (120, 120, 220) if self.home_button.collidepoint(mouse_pos) else (100, 100, 200)
            pygame.draw.rect(self.screen, color, self.home_button)
            home_text = self.font.render("HOME", True, (0, 0, 0))
            home_rect = home_text.get_rect(center=self.home_button.center)
            self.screen.blit(home_text, home_rect)
            
            # Verifica cliques
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                if self.next_button.collidepoint(mouse_pos):
                    return "next"
                elif self.restart_button.collidepoint(mouse_pos):
                    return "restart"
                elif self.home_button.collidepoint(mouse_pos):
                    return "home"
            
            pygame.display.flip()
    
    def reset(self):
        self.level_completed = False
        self.player_visible = True

    def draw(self):
        # Removido o overlay
        
        # Janela principal
        pygame.draw.rect(self.screen, self.window_color, 
                        (self.x, self.y, self.width, self.height))
        
        # Borda dupla
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.x, self.y, self.width, self.height), 3)
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 1)
        
        # Texto "LEVEL COMPLETED" com sombra
        title = self.font.render("LEVEL COMPLETED", True, self.title_color)
        shadow = self.font.render("LEVEL COMPLETED", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.game.window.width//2, self.y + 60))
        self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Botões com efeitos
        for button, text, colors in [
            (self.next_button, "NEXT", self.button_colors['next']),
            (self.restart_button, "RESTART", self.button_colors['restart']),
            (self.home_button, "HOME", self.button_colors['home'])
        ]:
            # Sombra do botão
            pygame.draw.rect(self.screen, (0, 0, 0, 100), 
                           (button.x + 2, button.y + 2, button.width, button.height))
            
            # Corpo do botão
            color = colors['hover'] if button.collidepoint(mouse_pos) else colors['normal']
            pygame.draw.rect(self.screen, color, button)
            pygame.draw.rect(self.screen, (255, 255, 255), button, 2)
            
            # Texto do botão
            text_surf = self.font_buttons.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=button.center)
            self.screen.blit(text_surf, text_rect)
        
        # Verifica cliques
        if pygame.mouse.get_pressed()[0]:
            if self.next_button.collidepoint(mouse_pos):
                return "next"
            elif self.restart_button.collidepoint(mouse_pos):
                return "restart"
            elif self.home_button.collidepoint(mouse_pos):
                return "home"
        
        return None
