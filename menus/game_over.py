import pygame
from settingsGame.settings_game import Fonts
class GameOver:
    def __init__(self, game, score):
        self.game = game
        self.screen = game.window.get_screen()
        self.score = score
        self.show_game_over = False
        self.player_visible = True
        
        # Configurações da janela
        self.width = 400
        self.height = 300
        self.x = (game.window.width - self.width) // 2
        self.y = (game.window.height - self.height) // 2
        
        # Cores
        self.window_color = (41, 41, 41)  # Cinza escuro
        self.border_color = (255, 198, 10)  # Dourado
        self.title_color = (255, 198, 10)  # Dourado
        self.score_color = (255, 198, 10)  # Dourado
        self.button_colors = {
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
        button_spacing = 20
        start_x = self.x + (self.width - button_width) // 2
        start_y = self.y + 150
        
        self.restart_button = pygame.Rect(start_x, start_y, button_width, button_height)
        self.home_button = pygame.Rect(start_x, start_y + button_height + button_spacing, button_width, button_height)
        
        # Fontes com Press Start 2P
        self.font = pygame.font.Font(Fonts["press_start"], 32)        # Título
        self.font_score = pygame.font.Font(Fonts["press_start"], 24)  # Score
        self.font_buttons = pygame.font.Font(Fonts["press_start"], 16) # Botões
    
    def draw(self):
        # Overlay semi-transparente
        overlay = pygame.Surface((self.game.window.width, self.game.window.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # Mais escuro
        self.screen.blit(overlay, (0, 0))
        
        # Janela principal com sombra
        shadow_offset = 4
        pygame.draw.rect(self.screen, (0, 0, 0, 100), 
                        (self.x + shadow_offset, self.y + shadow_offset, self.width, self.height))
        
        # Janela principal
        pygame.draw.rect(self.screen, self.window_color, 
                        (self.x, self.y, self.width, self.height))
        
        # Borda dupla
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.x, self.y, self.width, self.height), 3)
        pygame.draw.rect(self.screen, self.border_color, 
                        (self.x + 5, self.y + 5, self.width - 10, self.height - 10), 1)
        
        # Texto "GAME OVER" com sombra
        title = self.font.render("GAME OVER", True, self.title_color)
        shadow = self.font.render("GAME OVER", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.game.window.width//2, self.y + 60))
        self.screen.blit(shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Score com ícone de estrela
        score_text = self.font_score.render(f"Score: {self.score}", True, self.score_color)
        score_rect = score_text.get_rect(center=(self.game.window.width//2, self.y + 120))
        self.screen.blit(score_text, score_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Botões com efeitos
        for button, text, colors in [
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
            if self.restart_button.collidepoint(mouse_pos):
                return "restart"
            elif self.home_button.collidepoint(mouse_pos):
                return "home"
        
        return None
