import pygame
import os
import math
import random
from settingsGame.settings_game import GameSettings, Items, Sounds

class InstrucoesWindow:
    def __init__(self, game):
        self.game = game
        self.screen = game.window.get_screen()
        
        # Dimensões da janela de instruções - aumentadas para caber todo o conteúdo
        self.width = GameSettings["WINDOW_WIDTH"] - 100
        self.height = GameSettings["WINDOW_HEIGHT"] - 100
        self.x = (GameSettings["WINDOW_WIDTH"] - self.width) // 2
        self.y = (GameSettings["WINDOW_HEIGHT"] - self.height) // 2
        
        # Cores atualizadas para um esquema mais elegante
        """self.bg_color = (30, 33, 36)  # Cinza escuro moderno
        self.border_color = (255, 198, 10)  # Amarelo suave
        self.text_color = (255, 255, 255)  # Branco puro
        self.highlight_color = (0, 122, 255)  # Azul vibrante
        self.shadow_color = (20, 20, 20)  # Sombra suave"""

        # Cores atualizadas para um estilo mais vibrante e lúdico
        self.bg_color = (41, 128, 185)  # Azul vibrante
        self.border_color = (255, 198, 10)  # Amarelo dourado (mantido)
        self.text_color = (255, 255, 255)  # Branco (mantido)
        self.highlight_color = (46, 204, 113)  # Verde vibrante
        self.shadow_color = (25, 80, 115)  # Sombra do azul
        
        # Carrega os ícones necessários
        self.icon_size = (40, 40)
        self.key_icons = {
            "up": self.load_and_scale_image(Items["up"]),
            "left": self.load_and_scale_image(Items["left"]),
            "right": self.load_and_scale_image(Items["right"])
        }
        
        # Carrega os spritesheets dos coletáveis
        self.collectible_icons = {
            "coin": self.load_spritesheet(Items["coin"]),
            "potion": self.load_spritesheet(Items["potion"]),
            "key": self.load_spritesheet(Items["key"])
        }
        
        # Índices de animação para os coletáveis
        self.animation_indices = {
            "coin": 0,
            "potion": 0,
            "key": 0
        }
        
        # Velocidade da animação
        self.animation_speed = 0.2
        self.animation_time = 0
        
        # Carrega a fonte pixel art
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 24)
        self.text_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 16)
        self.small_font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 12)
        
        # Som de navegação
        # self.hover_sound = pygame.mixer.Sound(Sounds["collect"])  # Removido som de hover
        self.click_sound = pygame.mixer.Sound(Sounds["click"])
        
        # Botão de retorno
        self.back_button = {
            'rect': pygame.Rect(self.x + self.width - 150, 
                              self.y + self.height - 60, 120, 40),
            'color': self.highlight_color,
            'text': "VOLTAR",
            'is_hovered': False
        }
        
        # Efeito de flutuação
        self.float_offset = 0
        self.float_speed = 2
        
        # Efeito de brilho
        self.glow_value = 0
        self.glow_speed = 2
        
        # Lista de páginas reorganizada com conteúdo mais claro
        self.pages = [
            # Página 1 - Controles Básicos
            [
                {"text": "CONTROLES BÁSICOS", "type": "header"},
                {"text": "Use as setas para se mover", "type": "subheader"},
                {"text": "← Mover para esquerda", "keys": ["left"]},
                {"text": "→ Mover para direita", "keys": ["right"]},
                {"text": "↑ Pular", "keys": ["up"]},
                {"text": "Pressione ↑ duas vezes para pulo duplo!", "type": "tip"},
            ],
            # Página 2 - Coletáveis e Poder
            [
                {"text": "ITENS E PODERES", "type": "header"},
                {"text": "Colete itens para ficar mais forte", "type": "subheader"},
                {"text": "Moedas → Pontos extras", "icon": "coin"},
                {"text": "Poções → Escudo protetor", "icon": "potion"},
                {"text": "Chaves → Abrem portas", "icon": "key"},
                {"text": "Combine itens para maior pontuação!", "type": "tip"},
            ],
            # Página 3 - Dicas de Combate
            [
                {"text": "DICAS DE COMBATE", "type": "header"},
                {"text": "Aprenda a derrotar inimigos", "type": "subheader"},
                {"text": "• Pule sobre inimigos para derrotá-los"},
                {"text": "• Use poções para ganhar invencibilidade"},
                {"text": "• Colete chaves para progredir"},
                {"text": "Fique atento aos ataques dos inimigos!", "type": "tip"},
            ]
        ]
        
        self.current_page = 0
        self.total_pages = len(self.pages)
        
        # Botões de navegação
        button_width = 120
        button_height = 40
        
        self.prev_button = {
            'rect': pygame.Rect(self.x + 50, 
                              self.y + self.height - 60,
                              button_width, button_height),
            'color': self.highlight_color,
            'text': "ANTERIOR",
            'is_hovered': False
        }
        
        self.next_button = {
            'rect': pygame.Rect(self.x + self.width - button_width - 50,
                              self.y + self.height - 60,
                              button_width, button_height),
            'color': self.highlight_color,
            'text': "PRÓXIMO",
            'is_hovered': False
        }
        
        # Indicadores de página
        self.dot_radius = 5
        self.dot_spacing = 20
        self.dots_y = self.y + self.height - 30
        
        # Efeitos de partículas
        self.particles = []
        self.particle_colors = [
            (255, 215, 0),  # Dourado
            (255, 255, 255),  # Branco
            (65, 105, 225)   # Azul
        ]

    def load_and_scale_image(self, path):
        return pygame.transform.scale(
            pygame.image.load(path).convert_alpha(), 
            self.icon_size
        )

    def load_spritesheet(self, path):
        # Carrega o spritesheet completo
        sheet = pygame.image.load(path).convert_alpha()
        
        # Dimensões de cada frame
        frame_width = sheet.get_width() // 8  # 8 frames por spritesheet
        frame_height = sheet.get_height()
        
        frames = []
        # Extrai cada frame do spritesheet
        for i in range(8):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, self.icon_size)
            frames.append(frame)
        
        return frames

    def draw_text_with_shadow(self, text, font, x, y, color):
        # Desenha sombra
        shadow_surf = font.render(text, True, self.shadow_color)
        self.screen.blit(shadow_surf, (x + 2, y + 2))
        
        # Desenha texto
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))
        
        return text_surf.get_height()

    def draw_instruction_item(self, item, x, y):
        if item.get("type") == "header":
            # Desenha cabeçalho com destaque
            height = self.draw_text_with_shadow(
                item["text"],
                self.title_font,
                x,
                y + self.float_offset,
                self.border_color
            )
            return height + 30
        
        if item.get("type") == "subheader":
            # Desenha subcabeçalho com cor diferente
            height = self.draw_text_with_shadow(
                item["text"],
                self.text_font,
                x,
                y,
                self.highlight_color
            )
            return height + 25
        
        if item.get("type") == "tip":
            # Desenha dicas com estilo especial
            tip_rect = pygame.Rect(x - 10, y, self.width - 100, 30)
            pygame.draw.rect(self.screen, (*self.highlight_color, 30), tip_rect, border_radius=5)
            height = self.draw_text_with_shadow(
                item["text"],
                self.small_font,
                x,
                y + 8,
                self.border_color
            )
            return height + 35
        
        # Desenha itens normais com ícones
        if "keys" in item:
            key_x = x
            for key in item["keys"]:
                # Desenha círculo de fundo para as teclas
                pygame.draw.circle(self.screen, self.highlight_color, 
                                 (key_x + 20, y + 20), 22)
                self.screen.blit(self.key_icons[key], (key_x, y))
                key_x += 50
            text_x = key_x + 10
        else:
            text_x = x
        
        if "icon" in item:
            # Desenha ícones de coletáveis com fundo circular
            pygame.draw.circle(self.screen, (*self.highlight_color, 50),
                             (x + 20, y + 20), 25)
            icon_type = item["icon"]
            current_frame = self.collectible_icons[icon_type][self.animation_indices[icon_type]]
            self.screen.blit(current_frame, (x, y))
            text_x = x + 60
        
        height = self.draw_text_with_shadow(
            item["text"],
            self.small_font,
            text_x,
            y + 12,
            self.text_color
        )
        
        return height + 40

    def draw_navigation_button(self, button, enabled=True):
        alpha = 255 if enabled else 128
        
        # Desenha sombra
        pygame.draw.rect(
            self.screen,
            self.shadow_color,
            (button['rect'].x + 2, button['rect'].y + 2,
             button['rect'].width, button['rect'].height),
            border_radius=8
        )
        
        # Desenha o botão
        button_color = (255, 89, 94) if button['is_hovered'] and enabled else button['color']
        button_surface = pygame.Surface((button['rect'].width, button['rect'].height), pygame.SRCALPHA)
        button_surface.fill((*button_color[:3], alpha))
        pygame.draw.rect(
            button_surface,
            button_color,
            button_surface.get_rect(),
            border_radius=8
        )
        self.screen.blit(button_surface, button['rect'])
        
        # Desenha o texto
        text_surf = self.small_font.render(button['text'], True, self.text_color)
        text_rect = text_surf.get_rect(center=button['rect'].center)
        text_surface = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        text_surface.blit(text_surf, (0, 0))
        text_surface.set_alpha(alpha)
        self.screen.blit(text_surface, text_rect)

    def draw_page_indicators(self):
        total_width = (self.total_pages - 1) * self.dot_spacing
        start_x = self.x + (self.width - total_width) // 2
        
        for i in range(self.total_pages):
            x = start_x + i * self.dot_spacing
            
            # Efeito de pulso para o indicador atual
            if i == self.current_page:
                pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 2
                radius = self.dot_radius + pulse
            else:
                radius = self.dot_radius
            
            # Desenha sombra
            pygame.draw.circle(
                self.screen,
                self.shadow_color,
                (x + 1, self.dots_y + 1),
                radius
            )
            
            # Desenha o indicador
            color = self.border_color if i == self.current_page else self.highlight_color
            pygame.draw.circle(
                self.screen,
                color,
                (x, self.dots_y),
                radius
            )

    def draw(self):
        # Atualiza animações dos coletáveis
        self.animation_time += 1/60  # Assumindo 60 FPS
        if self.animation_time >= self.animation_speed:
            self.animation_time = 0
            for key in self.animation_indices:
                self.animation_indices[key] = (self.animation_indices[key] + 1) % 8

        # Atualiza efeitos
        self.float_offset = math.sin(pygame.time.get_ticks() / 500) * 3
        
        # Escurece o fundo
        dark_surface = pygame.Surface(
            (GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"])
        )
        dark_surface.fill((0, 0, 0))
        dark_surface.set_alpha(128)
        self.screen.blit(dark_surface, (0, 0))
        
        # Desenha o painel principal com sombra
        pygame.draw.rect(
            self.screen,
            self.shadow_color,
            (self.x + 4, self.y + 4, self.width, self.height),
            border_radius=12
        )
        
        # Desenha o painel principal com cor sólida
        pygame.draw.rect(
            self.screen,
            self.bg_color,  # Usando a cor cinza escuro original
            (self.x, self.y, self.width, self.height),
            border_radius=12
        )
        
        # Desenha a borda
        pygame.draw.rect(
            self.screen,
            self.border_color,
            (self.x, self.y, self.width, self.height),
            4,
            border_radius=12
        )
        
        # Desenha título
        title = "INSTRUÇÕES"
        title_surf = self.title_font.render(title, True, self.border_color)
        title_rect = title_surf.get_rect(
            centerx=self.x + self.width // 2,
            y=self.y + 20
        )
        
        # Sombra do título
        title_shadow = self.title_font.render(title, True, self.shadow_color)
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_surf, title_rect)
        
        # Linha decorativa abaixo do título
        line_y = title_rect.bottom + 10
        line_width = self.width - 100
        line_x = self.x + (self.width - line_width) // 2
        
        # Desenha linha com gradiente
        for i in range(line_width):
            progress = i / line_width
            alpha = int(255 * math.sin(progress * math.pi))
            color = (*self.border_color, alpha)
            pygame.draw.line(
                self.screen,
                color,
                (line_x + i, line_y),
                (line_x + i, line_y + 2)
            )
        
        # Desenha instruções da página atual
        current_y = self.y + 100
        for instruction in self.pages[self.current_page]:
            current_y += self.draw_instruction_item(
                instruction,
                self.x + 50,
                current_y
            )
        
        # Desenha botões de navegação
        self.draw_navigation_button(
            self.prev_button,
            enabled=self.current_page > 0
        )
        self.draw_navigation_button(
            self.next_button,
            enabled=self.current_page < self.total_pages - 1
        )
        
        # Desenha indicadores de página
        self.draw_page_indicators()

    def handle_click(self, pos):
        if self.prev_button['rect'].collidepoint(pos) and self.current_page > 0:
            self.click_sound.play()
            self.current_page -= 1
            return None
        
        if self.next_button['rect'].collidepoint(pos) and self.current_page < self.total_pages - 1:
            self.click_sound.play()
            self.current_page += 1
            return None
        
        if self.back_button['rect'].collidepoint(pos):
            self.click_sound.play()
            return True
        
        return None

    def handle_hover(self, pos):
        # Atualiza estado de hover dos botões de navegação
        self.prev_button['is_hovered'] = (
            self.prev_button['rect'].collidepoint(pos) and 
            self.current_page > 0
        )
            
        self.next_button['is_hovered'] = (
            self.next_button['rect'].collidepoint(pos) and 
            self.current_page < self.total_pages - 1
        )
            
        # Atualiza estado de hover do botão voltar
        self.back_button['is_hovered'] = self.back_button['rect'].collidepoint(pos)

    def run(self):
        running = True
        while running:
            # Limpa a tela com cor preta
            self.screen.fill((0, 0, 0))
            
            # Processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Clique esquerdo
                        if self.handle_click(event.pos):
                            return True
                
                if event.type == pygame.MOUSEMOTION:
                    self.handle_hover(event.pos)
            
            # Atualiza partículas
            self.update_particles()
            
            # Desenha a janela
            self.draw()
            
            # Atualiza a tela
            pygame.display.flip()
            
            # Controle de FPS
            pygame.time.Clock().tick(60)

    def update_particles(self):
        # Cria novas partículas
        if len(self.particles) < 50 and random.random() < 0.1:
            self.particles.append({
                'x': random.randint(self.x, self.x + self.width),
                'y': random.randint(self.y, self.y + self.height),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(2, 4),
                'color': random.choice(self.particle_colors),
                'alpha': 255
            })
        
        # Atualiza partículas existentes
        for particle in self.particles[:]:
            particle['y'] -= particle['speed']
            particle['alpha'] -= 2
            
            if particle['alpha'] <= 0:
                self.particles.remove(particle)

# Adicione este código no final do arquivo para executar diretamente
if __name__ == "__main__":
    pygame.init()
    
    # Cria uma janela temporária para teste
    screen = pygame.display.set_mode((GameSettings["WINDOW_WIDTH"], GameSettings["WINDOW_HEIGHT"]))
    pygame.display.set_caption("Instruções")
    
    # Cria um objeto game simplificado para teste
    class GameDummy:
        class Window:
            def get_screen(self):
                return screen
        
        def __init__(self):
            self.window = self.Window()
    
    # Cria e executa a janela de instruções
    game = GameDummy()
    instrucoes = InstrucoesWindow(game)
    instrucoes.run()
    
    pygame.quit()
