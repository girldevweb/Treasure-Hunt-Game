from PPlay.window import *
import pygame
import os
from settingsGame.settings_game import *

class Credits:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.keyboard = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        
        # Carregando fontes
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 32)
        self.font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
        self.small_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 16)
        
        # Cores atualizadas para combinar com o novo estilo
        self.bg_color = (30, 33, 36)  # Cinza escuro moderno
        self.border_color = (255, 198, 10)  # Amarelo suave
        self.text_color = (255, 255, 255)  # Branco
        self.highlight_color = (0, 122, 255)  # Azul vibrante
        self.shadow_color = (20, 20, 20)  # Sombra suave
        
        # Botão de voltar
        self.back_button = {
            "rect": pygame.Rect(50, 500, 120, 40),
            "text": "BACK",
            "hover": False
        }
        
        # Créditos atualizados
        self.credits = [
            {"text": "GAME CREDITS", "font": self.title_font, "color": self.border_color},
            {"text": "", "font": self.font, "color": self.text_color},
            {"text": "DEVELOPMENT", "font": self.font, "color": self.highlight_color},
            {"text": "Lead Programmers", "font": self.small_font, "color": self.text_color},
            {"text": "Ludimilla Duarte", "font": self.font, "color": self.border_color},
            {"text": "Hernold Paterne", "font": self.font, "color": self.border_color},
            {"text": "", "font": self.font, "color": self.text_color},
            {"text": "ASSETS", "font": self.font, "color": self.highlight_color},
            {"text": "Music & Sound Effects", "font": self.small_font, "color": self.text_color},
            {"text": "Pixabay", "font": self.font, "color": self.border_color},
            {"text": "", "font": self.font, "color": self.text_color},
            {"text": "Images & Sprites", "font": self.small_font, "color": self.text_color},
            {"text": "Itch.io", "font": self.font, "color": self.border_color},
            {"text": "", "font": self.font, "color": self.text_color},
            {"text": "SPECIAL THANKS", "font": self.font, "color": self.highlight_color},
            {"text": "God", "font": self.small_font, "color": self.text_color},
            {"text": "For not letting us give up", "font": self.font, "color": self.border_color},
            {"text": "on this project", "font": self.font, "color": self.border_color}
        ]
        
        # Animação (velocidade super reduzida)
        self.scroll_y = self.window.height
        self.scroll_speed = 0.15  # Velocidade extremamente lenta
        
    def draw_credits(self):
        y = self.scroll_y
        spacing = 40
        
        for credit in self.credits:
            text_surface = credit["font"].render(credit["text"], True, credit["color"])
            text_rect = text_surface.get_rect(center=(self.window.width/2, y))
            
            # Só desenha se estiver visível na tela
            if 0 <= y <= self.window.height:
                # Efeito de fade nas bordas
                if y < 100:
                    alpha = int((y / 100) * 255)
                elif y > self.window.height - 100:
                    alpha = int(((self.window.height - y) / 100) * 255)
                else:
                    alpha = 255
                
                text_surface.set_alpha(alpha)
                self.window.get_screen().blit(text_surface, text_rect)
            
            y += spacing
            
        # Reseta a posição quando todos os créditos passarem
        if self.scroll_y + (len(self.credits) * spacing) < 0:
            self.scroll_y = self.window.height
            
    def draw_button(self, button, color):
        # Sombra
        pygame.draw.rect(self.window.get_screen(), self.shadow_color,
                        (button["rect"].x + 4, button["rect"].y + 4,
                         button["rect"].width, button["rect"].height),
                        border_radius=8)
        
        # Botão
        pygame.draw.rect(self.window.get_screen(), color,
                        button["rect"], border_radius=8)
        
        if button["hover"]:
            pygame.draw.rect(self.window.get_screen(), self.border_color,
                           button["rect"], 3, border_radius=8)
        
        # Texto
        text = self.font.render(button["text"], True, self.text_color)
        text_rect = text.get_rect(center=button["rect"].center)
        self.window.get_screen().blit(text, text_rect)
        
    def run(self):
        while True:
            # Atualiza posição dos créditos
            self.scroll_y -= self.scroll_speed
            
            # Verifica hover no botão
            mouse_x, mouse_y = self.mouse.get_position()
            self.back_button["hover"] = self.back_button["rect"].collidepoint(mouse_x, mouse_y)
            
            # Verifica clique no botão
            if self.mouse.is_button_pressed(1) and self.back_button["hover"]:
                self.game.audio_manager.play_effect("click")
                self.game.current_state = self.game.MENU
                return
            
            # Desenha o fundo
            self.window.set_background_color(self.bg_color)
            
            # Desenha os elementos
            self.draw_credits()
            self.draw_button(self.back_button, self.highlight_color)
            
            self.window.update() 