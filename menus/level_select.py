from PPlay.window import *
import pygame
import os
import math
from levels.level1 import Level1
from levels.level2 import Level2
from levels.level3 import Level3
from settingsGame.settings_game import *
from screens.instrucoes import InstrucoesWindow

class LevelSelect:
    def __init__(self, game):
        self.game = game
        self.window = game.window
        self.keyboard = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        self.clock = pygame.time.Clock()
       
        # Adiciona o animation_timer aqui
        self.animation_timer = 0
       
        # Cores atualizadas
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 121, 241)
        self.LIGHT_BLUE = (18, 182, 231)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (128, 128, 128)
        self.GREEN = (17, 149, 9)
        self.RED = (255, 0, 0)
        self.YELLOW_BLACK = (255, 193, 51)
        
        # Novas cores para o estilo atualizado
        """self.bg_color = (30, 33, 36)  # Cinza escuro moderno
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
        self.locked_color = (128, 128, 128)  # Cinza para níveis bloqueados
       

        # Botão de ajuda (?)
        help_button_size = 40
        margin = 20
        self.help_button = {
            "rect": pygame.Rect(
                self.window.width - help_button_size - margin,  # X position
                margin,  # Y position
                help_button_size,  # Width
                help_button_size   # Height
            ),
            "color": self.BLUE,
            "hover_color": self.LIGHT_BLUE,
            "is_hovered": False
        }
    
        # Fonte para o símbolo de interrogação
        self.help_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
        # Calcula posições centralizadas
        window_center_x = self.window.width // 2
        cards_total_width = 500  # Largura total dos três cards (150 * 3 + espaços)
        start_x = window_center_x - (cards_total_width // 2)
       
        # Níveis com posições centralizadas
        self.levels = [
            {
                "number": 1,
                "name": "Floresta Sombria",
                "unlocked": True,
                "completed": False,
                "rect": pygame.Rect(start_x, 180, 150, 180)
            },
            {
                "number": 2,
                "name": "Cavernas dos Susurros",
                "unlocked": False,
                "completed": False,
                "rect": pygame.Rect(start_x + 175, 180, 150, 180)
            },
            {
                "number": 3,
                "name": "Templo Perdido",
                "unlocked": False,
                "completed": False,
                "rect": pygame.Rect(start_x + 350, 180, 150, 180)
            }
        ]
       
        # Botão de voltar centralizado na parte inferior
        back_button_width = 120
        back_button_height = 40
        self.back_button = {
            "rect": pygame.Rect(
                (self.window.width - back_button_width) // 2,
                500,  # Altura fixa do botão
                back_button_width,
                back_button_height
            ),
            "text": "BACK",
            "hover": False
        }
       
        self.selected_level = None
       
        # Carregando fontes
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 32)
        self.number_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 48)
        self.name_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 12)
        self.font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
       
        # Carrega o som de clique
        self.click_sound = pygame.mixer.Sound(os.path.join("game/sounds", "click.wav"))
       
        # Adicione um atributo para salvar o último nível completado
        self.last_completed_level = 0


    def draw_help_button(self):
        # Desenha sombra
        shadow_rect = self.help_button["rect"].copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.window.get_screen(), self.BLACK, shadow_rect, border_radius=8)
        
        # Desenha o botão
        color = self.help_button["hover_color"] if self.help_button["is_hovered"] else self.help_button["color"]
        pygame.draw.rect(self.window.get_screen(), color, self.help_button["rect"], border_radius=8)
        
        # Desenha a borda
        pygame.draw.rect(self.window.get_screen(), self.border_color, self.help_button["rect"], 2, border_radius=8)
        
        # Desenha o símbolo "?"
        text = self.help_font.render("?", True, self.WHITE)
        text_rect = text.get_rect(center=self.help_button["rect"].center)
        self.window.get_screen().blit(text, text_rect)

    def draw(self):
        # Limpa a tela
        self.window.set_background_color((45, 45, 45))
       
        # Desenha os botões
        for button in self.level_buttons:
            color = button["hover_color"] if button["rect"].collidepoint(pygame.mouse.get_pos()) else button["color"]
            if not button["unlocked"]:
                color = (70, 70, 70)  # Cor mais escura para níveis bloqueados
           
            pygame.draw.rect(self.window.get_screen(), color, button["rect"])
            pygame.draw.rect(self.window.get_screen(), (255, 255, 255), button["rect"], 2)
           
            # Renderiza o texto do botão
            font = pygame.font.Font(None, 36)
            text = font.render(button["text"], True, (255, 255, 255))
            text_rect = text.get_rect(center=button["rect"].center)
            self.window.get_screen().blit(text, text_rect)
           
            # Adiciona ícone de cadeado para níveis bloqueados
            if not button["unlocked"]:
                lock_text = font.render("🔒", True, (255, 255, 255))
                lock_rect = lock_text.get_rect(center=(button["rect"].centerx, button["rect"].centery + 30))
                self.window.get_screen().blit(lock_text, lock_rect)

    def draw_title(self):
        offset_y = math.sin(self.animation_timer * 2) * 3
        title_shadow = self.title_font.render("SELECT LEVEL", True, self.BLACK)
        title = self.title_font.render("SELECT LEVEL", True, self.YELLOW)
       
        # Centraliza o título horizontalmente
        title_x = (self.window.width - title.get_width()) // 2
        shadow_x = title_x + 4
        title_y = 50  # Ajusta a posição vertical do título
       
        self.window.get_screen().blit(title_shadow, (shadow_x, title_y + 4 + offset_y))
        self.window.get_screen().blit(title, (title_x, title_y + offset_y))

    def draw_level_card(self, level):
        # Determina as cores baseado no estado do nível
        if not level["unlocked"]:
            main_color = self.locked_color
            text_color = (100, 100, 100)
        elif level == self.selected_level:
            main_color = self.highlight_color
            text_color = self.text_color
        elif level["completed"]:
            main_color = (0, 150, 0)  # Verde mais escuro
            text_color = self.text_color
        else:
            main_color = (45, 48, 51)  # Cinza um pouco mais claro que o fundo
            text_color = self.text_color
        
        # Sombra do card
        shadow_rect = level["rect"].copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(self.window.get_screen(), self.shadow_color, shadow_rect, border_radius=10)
        
        # Card principal
        pygame.draw.rect(self.window.get_screen(), main_color, level["rect"], border_radius=10)
        
        # Borda do card
        border_color = self.border_color if level == self.selected_level else (60, 63, 66)
        pygame.draw.rect(self.window.get_screen(), border_color, level["rect"], 3, border_radius=10)
        
        if not level["unlocked"]:
            # Ícone de bloqueado com estilo atualizado
            lock_text = self.number_font.render("🔒", True, text_color)
            lock_rect = lock_text.get_rect(center=level["rect"].center)
            self.window.get_screen().blit(lock_text, lock_rect)
        else:
            # Número do nível
            number_text = self.number_font.render(str(level["number"]), True, text_color)
            number_rect = number_text.get_rect(center=(level["rect"].centerx, level["rect"].centery - 20))
            self.window.get_screen().blit(number_text, number_rect)
            
            # Nome do nível
            words = level["name"].split()
            y_offset = 30
            
            for word in words:
                name_text = self.name_font.render(word, True, text_color)
                name_rect = name_text.get_rect(center=(level["rect"].centerx, level["rect"].centery + y_offset))
                self.window.get_screen().blit(name_text, name_rect)
                y_offset += 20

    def draw_button(self, button, color):
        # Sombra
        pygame.draw.rect(self.window.get_screen(), self.BLACK,
                        (button["rect"].x + 4, button["rect"].y + 4,
                         button["rect"].width, button["rect"].height),
                        border_radius=8)
       
        # Botão
        pygame.draw.rect(self.window.get_screen(), color,
                        button["rect"], border_radius=8)
       
        if button["hover"]:
            pygame.draw.rect(self.window.get_screen(), self.YELLOW,
                           button["rect"], 3, border_radius=8)
       
        # Texto
        text = self.font.render(button["text"], True, self.WHITE)
        text_rect = text.get_rect(center=button["rect"].center)
        self.window.get_screen().blit(text, text_rect)

    def unlock_next_level(self, completed_level):
        """Desbloqueia o próximo nível após completar um nível"""
        if completed_level > self.last_completed_level:
            self.last_completed_level = completed_level
           
            # Marca o nível atual como completado
            self.levels[completed_level - 1]["completed"] = True
           
            # Desbloqueia o próximo nível se existir
            if completed_level < len(self.levels):
                self.levels[completed_level]["unlocked"] = True
   
    def run(self):
        while True:
            self.clock.tick(60)
            self.animation_timer += 0.1
            
            # Fundo sólido
            self.window.set_background_color(self.bg_color)
            
            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        mouse_pos = pygame.mouse.get_pos()


                         # Verifica clique no botão de ajuda
                        if self.help_button["rect"].collidepoint(mouse_pos):
                            self.click_sound.play()
                            instrucoes = InstrucoesWindow(self.game)
                            instrucoes.run()
                            continue
                        
                       
                        # Verifica clique no botão de voltar
                        if self.back_button["rect"].collidepoint(mouse_pos):
                            self.click_sound.play()
                            self.game.current_state = self.game.MENU
                            return "menu"
                       
                         # Verifica clique nos níveis
                        for level in self.levels:
                            if level["rect"].collidepoint(mouse_pos) and level["unlocked"]:
                                self.click_sound.play()
                                if level["number"] == 1:
                                    level1 = Level1(self.game)
                                    result = level1.run()
                                    if result == "level2":
                                        self.unlock_next_level(1)
                                    return
                                elif level["number"] == 2:
                                    level2 = Level2(self.game)
                                    result = level2.run()
                                    if result == "level3":
                                        self.unlock_next_level(2)
                                    return
                                elif level["number"] == 3:
                                    level3 = Level3(self.game)
                                    result = level3.run()
                                    if result == "menu":
                                        return
           
            # Verifica ESC para voltar ao menu
            if self.keyboard.key_pressed("ESC"):
                self.click_sound.play()
                self.game.current_state = self.game.MENU
                return "menu"
           
            # Atualiza hover
            mouse_pos = pygame.mouse.get_pos()
            self.back_button["hover"] = self.back_button["rect"].collidepoint(mouse_pos)
            self.help_button["is_hovered"] = self.help_button["rect"].collidepoint(mouse_pos)
            
            # Atualiza seleção de nível
            for level in self.levels:
                if level["rect"].collidepoint(mouse_pos):
                    self.selected_level = level
                    break
                else:
                    if level == self.selected_level:
                        self.selected_level = None
            
            # Desenha elementos
            self.draw_title()
            for level in self.levels:
                self.draw_level_card(level)
            self.draw_button(self.back_button, 
                            self.highlight_color if not self.back_button["hover"] 
                            else (0, 140, 255))
            self.draw_help_button()
            
            # Atualiza a tela
            self.window.update()

    def handle_level_selection(self, level_number):
        if level_number == 1:
            level = Level1(self.game)
            return level.run()

