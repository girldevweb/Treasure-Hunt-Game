from PPlay.window import *
from PPlay.gameimage import *
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
import pygame
from settingsGame.settings_game import GameSettings, Items
import os

class SettingsMenu:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.screen = self.window.get_screen()
        self.mouse = Mouse()  # Usando a classe Mouse do pplay diretamente
        self.keyboard = Keyboard()  # Inicializa o teclado
        
        # Dimensões e posição do menu
        self.width = 300
        self.height = 350
        self.x = (GameSettings["WINDOW_WIDTH"] - self.width) // 2
        self.y = (GameSettings["WINDOW_HEIGHT"] - self.height) // 2
        
        # Cores mantidas do original
        self.bg_color = (41, 41, 41)
        self.border_color = (255, 215, 0)
        self.text_color = (255, 255, 255)
        self.button_color = (70, 70, 70)
        self.button_hover_color = (100, 100, 100)
        self.shadow_color = (20, 20, 20)
        self.title_glow = (255, 223, 91)
        
        # Carrega os ícones
        icon_size = (30, 30)
        self.icons = {
            'home': pygame.transform.scale(pygame.image.load(Items["home"]).convert_alpha(), icon_size),
            'audio': pygame.transform.scale(pygame.image.load(Items["audio_on"]).convert_alpha(), icon_size),
            'audio_off': pygame.transform.scale(pygame.image.load(Items["audio_off"]).convert_alpha(), icon_size),
            'play': pygame.transform.scale(pygame.image.load(Items["play"]).convert_alpha(), icon_size)
        }
        
        # Configuração dos botões (mantido pygame.Rect)
        button_y_start = self.y + 120
        button_spacing = 70
        button_width = 180
        button_height = 50
        center_x = self.x + self.width//2
        
        # Dicionário de botões com todas as informações
        self.buttons = {
            'home': {
                'rect': pygame.Rect(0, 0, button_width, button_height),
                'shadow_rect': pygame.Rect(0, 0, button_width, button_height),
                'text': "MENU",
                'icon': 'home',
                'is_hovered': False
            },
            'audio': {
                'rect': pygame.Rect(0, 0, button_width, button_height),
                'shadow_rect': pygame.Rect(0, 0, button_width, button_height),
                'text': "SOUND",
                'icon': 'audio',
                'is_hovered': False
            },
            'play': {
                'rect': pygame.Rect(0, 0, button_width, button_height),
                'shadow_rect': pygame.Rect(0, 0, button_width, button_height),
                'text': "CONTINUE",
                'icon': 'play',
                'is_hovered': False
            }
        }
        
        # Posiciona os botões
        for i, (key, button) in enumerate(self.buttons.items()):
            button['rect'].center = (center_x, button_y_start + i * button_spacing)
            button['shadow_rect'] = button['rect'].copy()
            button['shadow_rect'].y += 4
        
        # Referência ao AudioManager
        self.audio_manager = game.audio_manager
        
        # Fonte pixel art
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
        self.button_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 12)

    def handle_hover(self):
        """Atualiza o estado de hover dos botões usando Mouse do pplay"""
        mouse_pos = self.mouse.get_position()
        for button in self.buttons.values():
            button['is_hovered'] = button['rect'].collidepoint(mouse_pos)

    def handle_click(self):
        """Gerencia os cliques nos botões usando Mouse do pplay"""
        if self.mouse.is_button_pressed(1):  # Botão esquerdo
            mouse_pos = self.mouse.get_position()
            for action, button in self.buttons.items():
                if button['rect'].collidepoint(mouse_pos):
                    if not self.audio_manager.is_muted:
                        self.audio_manager.play_effect("click")
                    
                    # Caso especial para o botão de áudio
                    if action == 'audio':
                        self.audio_manager.toggle_mute()
                    
                    # Mapeia diretamente as ações
                    actions = {
                        'home': 'home',
                        'audio': 'audio',
                        'play': 'continue'
                    }
                    return actions.get(action)
        return None

    def draw_button(self, button, is_audio_button=False):
        # Desenha sombra do botão
        pygame.draw.rect(self.screen, self.shadow_color, button['shadow_rect'], border_radius=8)
        
        # Desenha o botão principal com efeito de brilho quando hover
        button_color = self.button_hover_color if button['is_hovered'] else self.button_color
        if button['is_hovered']:
            # Brilho do botão
            glow_rect = button['rect'].copy()
            glow_rect.inflate_ip(4, 4)
            pygame.draw.rect(self.screen, self.title_glow, glow_rect, border_radius=8)
        
        pygame.draw.rect(self.screen, button_color, button['rect'], border_radius=8)
        
        # Borda dourada dos botões
        border_rects = [
            (button['rect'].left, button['rect'].top, button['rect'].width, 2),
            (button['rect'].left, button['rect'].bottom-2, button['rect'].width, 2),
            (button['rect'].left, button['rect'].top, 2, button['rect'].height),
            (button['rect'].right-2, button['rect'].top, 2, button['rect'].height)
        ]
        for border_rect in border_rects:
            pygame.draw.rect(self.screen, self.border_color, border_rect)
        
        # Seleciona o ícone correto para o botão de áudio
        icon = None
        if is_audio_button:
            icon = self.icons['audio'] if not self.audio_manager.is_muted else self.icons['audio_off']
        else:
            icon = self.icons[button['icon']]
        
        # Desenha o ícone
        icon_x = button['rect'].left + 20
        icon_y = button['rect'].centery - icon.get_height()//2
        self.screen.blit(icon, (icon_x, icon_y))
        
        # Desenha o texto com sombra
        text_surf = self.button_font.render(button['text'], True, self.text_color)
        text_rect = text_surf.get_rect(midleft=(icon_x + icon.get_width() + 10, button['rect'].centery))
        
        # Sombra do texto
        text_shadow = self.button_font.render(button['text'], True, self.shadow_color)
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        self.screen.blit(text_shadow, shadow_rect)
        self.screen.blit(text_surf, text_rect)

    def draw(self):
        # Escurece o fundo com mais transparência
        dark_surface = pygame.Surface((GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"]))
        dark_surface.fill((0, 0, 0))
        dark_surface.set_alpha(160)  # Aumentado para 160
        self.screen.blit(dark_surface, (0, 0))
        
        # Desenha o painel principal com sombra mais suave
        pygame.draw.rect(self.screen, self.shadow_color,
                       (self.x+4, self.y+4, self.width, self.height), border_radius=12)
        pygame.draw.rect(self.screen, self.bg_color,
                       (self.x, self.y, self.width, self.height), border_radius=12)
        
        # Borda dourada com brilho
        border_rects = [
            (self.x, self.y, self.width, 4),
            (self.x, self.y+self.height-4, self.width, 4),
            (self.x, self.y, 4, self.height),
            (self.x+self.width-4, self.y, 4, self.height)
        ]
        
        # Desenha borda com efeito de brilho
        for border_rect in border_rects:
            # Borda externa (brilho)
            pygame.draw.rect(self.screen, self.title_glow, 
                           (border_rect[0]-1, border_rect[1]-1, 
                            border_rect[2]+2, border_rect[3]+2))
            # Borda principal
            pygame.draw.rect(self.screen, self.border_color, border_rect)
        
        # Desenha o título com efeito de brilho
        title = self.title_font.render("SETTINGS", True, self.text_color)
        title_glow = self.title_font.render("SETTINGS", True, self.title_glow)
        
        title_rect = title.get_rect(center=(self.x + self.width//2, self.y + 60))
        
        # Desenha o brilho do título
        glow_rect = title_rect.copy()
        for offset in [(1,1), (-1,-1), (1,-1), (-1,1)]:
            glow_rect.x = title_rect.x + offset[0]
            glow_rect.y = title_rect.y + offset[1]
            self.screen.blit(title_glow, glow_rect)
        
        # Desenha o título principal
        self.screen.blit(title, title_rect)
        
        # Atualiza hover dos botões
        self.handle_hover()
        
        # Desenha os botões
        for key, button in self.buttons.items():
            self.draw_button(button, is_audio_button=(key == 'audio'))

    def handle_input(self):
        """Gerencia input do teclado e mouse"""
        # Verifica tecla ESC
        if self.keyboard.key_pressed("ESC"):
            if not self.audio_manager.is_muted:
                self.audio_manager.play_effect("click")
            return "continue"
        
        # Verifica cliques do mouse
        return self.handle_click()

    def run(self):
        while True:
            # Atualiza hover dos botões
            self.handle_hover()
            
            # Verifica input
            result = self.handle_input()
            if result:
                return result
            
            # Desenha o menu
            self.draw()
            
            # Atualiza a tela
            self.window.update()
