from PPlay.window import *
from PPlay.gameimage import *
from PPlay.keyboard import *

import os



class Menu:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.keyboard = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        
        # Carregando a fonte
        font_path = os.path.join("game/fonts", "PressStart2P.ttf")
        self.title_font = pygame.font.Font(font_path, 48)
        self.button_font = pygame.font.Font(font_path, 20)
        
        
        
        """# Cores atualizadas para combinar com o novo estilo
        self.bg_color = (30, 33, 36)  # Cinza escuro moderno
        self.border_color = (255, 198, 10)  # Amarelo suave
        self.text_color = (255, 255, 255)  # Branco
        self.highlight_color = (0, 122, 255)  # Azul vibrante
        self.shadow_color = (20, 20, 20)  # Sombra suave"""

        # Cores atualizadas para um estilo mais vibrante e lúdico
        self.bg_color = (41, 128, 185)  # Azul vibrante
        self.border_color = (255, 198, 10)  # Amarelo dourado (mantido)
        self.text_color = (255, 255, 255)  # Branco (mantido)
        self.highlight_color = (46, 204, 113)  # Verde vibrante
        self.shadow_color = (25, 80, 115)  # Sombra do azul
        
        # Configurações dos botões
        self.button_width = 280
        self.button_height = 50
        button_y = 250
        button_spacing = 70
        
        # Lista de botões
        self.buttons = []
        button_texts = ["START", "SETTINGS", "CREDITS", "EXIT"]
        
        for i, text in enumerate(button_texts):
            button = {
                "text": text,
                "x": self.window.width/2 - self.button_width/2,
                "y": button_y + (i * button_spacing),
                "width": self.button_width,
                "height": self.button_height,
                "selected": False,
                "hover": False
            }
            self.buttons.append(button)
        
        self.selected_button = 0
        
        # Carrega o som de clique
        self.click_sound = pygame.mixer.Sound(os.path.join("game/sounds", "click.wav"))
        
        # Inicia a música do menu
        self.game.audio_manager.stop_music()  # Para qualquer música atual
        self.game.audio_manager._in_intro = True  # Define que estamos na intro
        self.game.audio_manager.play_music("intro") 
        
    def draw_title(self):
        title_text = "TREASURE HUNT"
        
        # Desenha sombra do título
        shadow_surface = self.title_font.render(title_text, True, self.shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(self.window.width/2 + 4, 104))
        self.window.get_screen().blit(shadow_surface, shadow_rect)
        
        # Desenha título
        title_surface = self.title_font.render(title_text, True, self.border_color)
        title_rect = title_surface.get_rect(center=(self.window.width/2, 100))
        self.window.get_screen().blit(title_surface, title_rect)
        
    def draw_buttons(self):
        for i, button in enumerate(self.buttons):
            x = button["x"]
            y = button["y"]
            
            # Atualiza estado do botão
            button["selected"] = (i == self.selected_button)
            button["hover"] = (
                x <= self.mouse.get_position()[0] <= x + button["width"] and
                y <= self.mouse.get_position()[1] <= y + button["height"]
            )
            
            # Desenha sombra do botão
            shadow_rect = pygame.Rect(x + 4, y + 4, button["width"], button["height"])
            pygame.draw.rect(
                self.window.get_screen(),
                self.shadow_color,
                shadow_rect,
                border_radius=8
            )
            
            # Determina a cor do botão
            if button["selected"] or button["hover"]:
                button_color = self.highlight_color
            else:
                button_color = (45, 48, 51)  # Cinza um pouco mais claro que o fundo
            
            # Desenha o botão principal
            button_rect = pygame.Rect(x, y, button["width"], button["height"])
            pygame.draw.rect(
                self.window.get_screen(),
                button_color,
                button_rect,
                border_radius=8
            )
            
            # Desenha a borda
            border_color = self.border_color if button["selected"] or button["hover"] else (60, 63, 66)
            pygame.draw.rect(
                self.window.get_screen(),
                border_color,
                button_rect,
                3,
                border_radius=8
            )
            
            # Desenha o texto do botão
            text = self.button_font.render(button["text"], True, self.text_color)
            text_rect = text.get_rect(center=(x + button["width"]/2, y + button["height"]/2))
            self.window.get_screen().blit(text, text_rect)
    
    def run(self):



            # Garante que a música está tocando
        if not self.game.audio_manager.is_muted and not self.game.audio_manager._is_playing:
            self.game.audio_manager.play_music("intro")

        while True:
            # Limpa a tela com a cor de fundo
            self.window.set_background_color(self.bg_color)
            
            # Input handling
            if self.keyboard.key_pressed("UP"):
                self.click_sound.play()
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
                self.window.delay(150)
                
            if self.keyboard.key_pressed("DOWN"):
                self.click_sound.play()
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
                self.window.delay(150)
            
            if self.keyboard.key_pressed("RETURN"):
                self.click_sound.play()
                if self.selected_button == 0:  # START
                    self.game.current_state = self.game.LEVEL_SELECT
                    return
                elif self.selected_button == 1:  # SETTINGS
                    self.game.current_state = self.game.SETTINGS
                    return
                elif self.selected_button == 2:  # CREDITS
                    self.game.current_state = self.game.CREDITS
                    return
                elif self.selected_button == 3:  # EXIT
                    self.window.close()
                    return
            
            # Verificação do mouse
            if self.mouse.is_button_pressed(1):  # Botão esquerdo do mouse
                mouse_x, mouse_y = self.mouse.get_position()
                for i, button in enumerate(self.buttons):
                    if (button["x"] <= mouse_x <= button["x"] + button["width"] and
                        button["y"] <= mouse_y <= button["y"] + button["height"]):
                        self.click_sound.play()
                        self.selected_button = i
                        if i == 3:  # EXIT
                            self.window.close()
                            return
                        else:
                            self.game.current_state = [
                                self.game.LEVEL_SELECT,
                                self.game.SETTINGS,
                                self.game.CREDITS
                            ][i]
                            return
            
            # Desenha elementos
            self.draw_title()
            self.draw_buttons()
            
            # Atualiza a tela
            self.window.update() 