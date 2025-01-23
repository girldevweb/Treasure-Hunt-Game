import pygame
import os
from settingsGame.settings_game import GameSettings, Items

class FinalLevel:
    def __init__(self, game, final_score):
        self.game = game
        self.screen = game.window.get_screen()
        self.final_score = final_score
        
        # Dimensões e posição do painel
        self.width = 600
        self.height = 500
        self.x = (GameSettings["WINDOW_WIDTH"] - self.width) // 2
        self.y = (GameSettings["WINDOW_HEIGHT"] - self.height) // 2
        
      

         # Cores atualizadas para combinar com Level Completed
        self.bg_color = (41, 41, 41)  # Cinza escuro
        self.border_color = (255, 198, 10)  # Mesma cor dourada do Level Completed
        self.text_color = (255, 198, 10)  # Título e score agora usam a mesma cor dourada
        self.button_color = (70, 70, 70)  # Cinza médio
        self.button_hover_color = (100, 100, 100)  # Cinza claro
        self.shadow_color = (20, 20, 20)  # Sombra mais escura
        self.title_glow = (255, 223, 91)  # Brilho dourado
        
        
        # Carrega os ícones
        icon_size = (30, 30)
        self.home_img = pygame.transform.scale(
            pygame.image.load(Items["home"]).convert_alpha(), icon_size)
        
        # Configuração dos botões
        button_width = 180
        button_height = 50
        center_x = self.x + self.width//2
        button_y = self.y + self.height - 80
        
        # Retângulo do botão home
        self.home_rect = pygame.Rect(0, 0, button_width, button_height)
        self.home_rect.center = (center_x, button_y)
        self.home_shadow = self.home_rect.copy()
        self.home_shadow.y += 4
        
        # Fonte pixel art
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 24)
        self.text_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 14)
        self.button_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 12)
        
        # Carrega o som de clique
        self.click_sound = pygame.mixer.Sound(os.path.join("game/sounds", "click.wav"))
        
        # Texto da história final
        self.story_text = [
            
            
            "Após enfrentar inúmeros perigos,",
            "derrotar criaturas místicas e",
            "superar todos os obstáculos,",
            "você provou ser digno ",
            "do tesouro perdido",
            "Sua coragem e determinação",
            "tornaram você uma lenda!"


        ]
        
        # Texto do score
        self.score_text = f"Score Final: {self.final_score}"

    def draw_button(self, rect, shadow_rect, icon, text, is_hovered=False):
        # Desenha sombra do botão
        pygame.draw.rect(self.screen, self.shadow_color, shadow_rect, border_radius=8)
        
        # Desenha o botão principal
        button_color = self.button_hover_color if is_hovered else self.button_color
        
        # Adiciona brilho quando hover
        if is_hovered:
            glow_rect = rect.copy()
            glow_rect.inflate_ip(4, 4)
            pygame.draw.rect(self.screen, self.title_glow, glow_rect, border_radius=8)
        
        pygame.draw.rect(self.screen, button_color, rect, border_radius=8)
        
        # Borda dourada dos botões
        border_rects = [
            (rect.left, rect.top, rect.width, 2),
            (rect.left, rect.bottom-2, rect.width, 2),
            (rect.left, rect.top, 2, rect.height),
            (rect.right-2, rect.top, 2, rect.height)
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
        # Escurece o fundo
        dark_surface = pygame.Surface((GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"]))
        dark_surface.fill((0, 0, 0))
        dark_surface.set_alpha(160)
        self.screen.blit(dark_surface, (0, 0))
        
        # Desenha o painel principal com sombra
        pygame.draw.rect(self.screen, self.shadow_color, 
                       (self.x+4, self.y+4, self.width, self.height), border_radius=12)
        pygame.draw.rect(self.screen, self.bg_color, 
                       (self.x, self.y, self.width, self.height), border_radius=12)
        
        # Borda dourada
        border_rects = [
            (self.x, self.y, self.width, 4),
            (self.x, self.y+self.height-4, self.width, 4),
            (self.x, self.y, 4, self.height),
            (self.x+self.width-4, self.y, 4, self.height)
        ]
        
        # Desenha apenas a borda dourada, sem brilho
        for border_rect in border_rects:
            pygame.draw.rect(self.screen, self.border_color, border_rect)
        
        # Desenha o título "Parabéns!" com sombra
        title = self.title_font.render("Parabéns!", True, self.text_color)
        title_shadow = self.title_font.render("Parabéns!", True, self.shadow_color)
        
        title_rect = title.get_rect(center=(self.x + self.width//2, self.y + 60))
        shadow_rect = title_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        
        # Desenha a sombra e o título
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # Desenha o texto da história
        y_offset = self.y + 120
        for line in self.story_text:
            if line:  # Só desenha se a linha não estiver vazia
                text_surf = self.text_font.render(line, True, self.text_color)
                text_rect = text_surf.get_rect(center=(self.x + self.width//2, y_offset))
                self.screen.blit(text_surf, text_rect)
            y_offset += 30
        
        # Desenha o score com sombra
        score_surf = self.text_font.render(self.score_text, True, self.text_color)
        score_shadow = self.text_font.render(self.score_text, True, self.shadow_color)
        
        score_rect = score_surf.get_rect(center=(self.x + self.width//2, y_offset + 20))
        shadow_rect = score_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        
        # Desenha a sombra e o score
        self.screen.blit(score_shadow, shadow_rect)
        self.screen.blit(score_surf, score_rect)
        
        # Verifica hover do botão
        mouse_pos = pygame.mouse.get_pos()
        home_hover = self.home_rect.collidepoint(mouse_pos)
        
        # Desenha o botão
        self.draw_button(self.home_rect, self.home_shadow, self.home_img, "MENU", home_hover)

    def update(self):
        """Atualiza a tela final usando a mesma lógica do LevelManager"""
        # Verifica clique do mouse
        if pygame.mouse.get_pressed()[0]:  # Botão esquerdo do mouse
            mouse_pos = pygame.mouse.get_pos()
            if self.home_rect.collidepoint(mouse_pos):
                self.click_sound.play()
                return "menu"
        
        # Desenha a tela
        self.draw()
        return None
