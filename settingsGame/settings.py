from PPlay.window import *
import pygame
import os

from settingsGame.settings_game import *

class Settings:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.keyboard = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        
        # Carregando fontes
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 32)
        self.font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
        
        # Cores atualizadas para combinar com o novo estilo
        self.bg_color = (30, 33, 36)  # Cinza escuro moderno
        self.border_color = (255, 198, 10)  # Amarelo suave
        self.text_color = (255, 255, 255)  # Branco
        self.highlight_color = (0, 122, 255)  # Azul vibrante
        self.shadow_color = (20, 20, 20)  # Sombra suave
        self.slider_bg_color = (45, 48, 51)  # Cinza um pouco mais claro que o fundo
        
        # Configurações
        self.volume = pygame.mixer.music.get_volume() * 100 if pygame.mixer.music.get_busy() else 100
        self.bgm_enabled = True  # Nova configuração para música de fundo
        
        # Som de clique para feedback
        self.click_sound = pygame.mixer.Sound(os.path.join("game/sounds", "click.wav"))
        
        # Elementos da interface
        self.slider_width = 300
        self.slider_height = 20
        self.slider_x = self.window.width/2 - self.slider_width/2
        self.slider_y = 250
        
        self.button_width = 280
        self.button_height = 50
        
        # Botões
        self.bgm_button = {
            "rect": pygame.Rect(self.window.width/2 - self.button_width/2,
                              350, self.button_width, self.button_height),
            "text": "MUSIC: ON" if self.bgm_enabled else "MUSIC: OFF",
            "hover": False
        }
        
        self.back_button = {
            "rect": pygame.Rect(50, 500,
                              120, 40),
            "text": "BACK",
            "hover": False
        }
        
        self.dragging_slider = False
        
        # Salva as configurações originais caso o usuário cancele
        self.original_volume = self.volume
        self.original_bgm = self.bgm_enabled
        
    def draw_title(self):
        # Desenha sombra do título
        title_shadow = self.title_font.render("SETTINGS", True, self.shadow_color)
        title = self.title_font.render("SETTINGS", True, self.border_color)
        
        self.window.get_screen().blit(title_shadow,
            (self.window.width/2 - title_shadow.get_width()/2 + 4, 104))
        self.window.get_screen().blit(title,
            (self.window.width/2 - title.get_width()/2, 100))
        
    def draw_volume_slider(self):
        # Sombra do slider
        pygame.draw.rect(self.window.get_screen(), self.shadow_color,
                        (self.slider_x + 4, self.slider_y + 4,
                         self.slider_width, self.slider_height),
                        border_radius=10)
        
        # Barra de fundo
        pygame.draw.rect(self.window.get_screen(), self.slider_bg_color,
                        (self.slider_x, self.slider_y,
                         self.slider_width, self.slider_height),
                        border_radius=10)
        
        # Barra de progresso
        progress_width = (self.slider_width * self.volume) // 100
        pygame.draw.rect(self.window.get_screen(), self.highlight_color,
                        (self.slider_x, self.slider_y,
                         progress_width, self.slider_height),
                        border_radius=10)
        
        # Knob do slider
        knob_x = self.slider_x + progress_width - 10
        # Sombra do knob
        pygame.draw.circle(self.window.get_screen(), self.shadow_color,
                         (knob_x + 2, self.slider_y + self.slider_height/2 + 2), 15)
        # Knob principal
        pygame.draw.circle(self.window.get_screen(), self.border_color,
                         (knob_x, self.slider_y + self.slider_height/2), 15)
        
        # Texto do volume
        volume_text = self.font.render(f"VOLUME: {self.volume}%", True, self.text_color)
        self.window.get_screen().blit(volume_text,
            (self.slider_x, self.slider_y - 40))
        
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
        
    def apply_volume(self):
        """Aplica o volume atual usando o AudioManager"""
        self.game.audio_manager.set_volume(self.volume)
        
    def toggle_bgm(self):
        """Alterna a música de fundo usando o AudioManager"""
        self.bgm_enabled = not self.bgm_enabled
        self.game.audio_manager.toggle_bgm(self.bgm_enabled)
        self.bgm_button["text"] = "MUSIC: ON" if self.bgm_enabled else "MUSIC: OFF"
        
    def save_settings(self):
        """Salva as configurações em um arquivo"""
        settings = {
            "volume": self.volume,
            "bgm": self.bgm_enabled
        }
        
        try:
            with open("game/settings.txt", "w") as f:
                f.write(f"volume={settings['volume']}\n")
                f.write(f"bgm={1 if settings['bgm'] else 0}\n")
        except:
            print("Erro ao salvar configurações")
        
    def load_settings(self):
        """Carrega as configurações salvas"""
        try:
            with open("game/settings.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key == "volume":
                        self.volume = float(value)
                    elif key == "bgm":
                        self.bgm_enabled = bool(int(value))
            
            # Aplica as configurações carregadas
            self.apply_volume()
            if not self.bgm_enabled:
                pygame.mixer.music.pause()
        except:
            print("Arquivo de configurações não encontrado, usando padrões")
        
    def run(self):
        # Carrega configurações salvas ao abrir a janela
        self.load_settings()
        
        while True:
            mouse_x, mouse_y = self.mouse.get_position()
            mouse_pressed = self.mouse.is_button_pressed(1)
            
            # Verifica hover nos botões
            self.bgm_button["hover"] = self.bgm_button["rect"].collidepoint(mouse_x, mouse_y)
            self.back_button["hover"] = self.back_button["rect"].collidepoint(mouse_x, mouse_y)
            
            # Controle do slider
            if mouse_pressed:
                if (self.slider_y <= mouse_y <= self.slider_y + self.slider_height and
                    self.slider_x <= mouse_x <= self.slider_x + self.slider_width):
                    self.volume = int(((mouse_x - self.slider_x) / self.slider_width) * 100)
                    self.volume = max(0, min(100, self.volume))
                    self.apply_volume()  # Aplica o volume em tempo real
                
                # Clique nos botões
                if self.bgm_button["hover"]:
                    self.click_sound.play()
                    self.toggle_bgm()
                    self.window.delay(200)
                elif self.back_button["hover"]:
                    self.click_sound.play()
                    self.save_settings()  # Salva as configurações ao sair
                    self.game.current_state = self.game.MENU
                    return
            
            # Tecla ESC para cancelar alterações
            if self.keyboard.key_pressed("ESC"):
                self.volume = self.original_volume
                if self.bgm_enabled != self.original_bgm:
                    self.toggle_bgm()
                self.apply_volume()
                self.game.current_state = self.game.MENU
                return
            
            # Desenha elementos
            self.window.set_background_color(self.bg_color)
            
            self.draw_title()
            self.draw_volume_slider()
            self.draw_button(self.bgm_button,
                           self.highlight_color if self.bgm_enabled else self.slider_bg_color)
            self.draw_button(self.back_button, self.slider_bg_color)
            
            self.window.update() 