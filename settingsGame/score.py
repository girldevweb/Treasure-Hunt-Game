from PPlay.window import *
import pygame
import os

class ScoreSystem:
    def __init__(self, window):
        # Pontuação inicial
        self.score = 0
        self.window = window
        
        # Pontos por tipo de inimigo
        self.enemy_points = {
            "duende": 100,
            "cogumelo": 150,
            "goblin": 200,
            "boss": 1000,
            "treasure": 500,
            "bat": 100,
            "snake": 50,
            "goblin_king": 200,
            "minotaur": 250,
            "brain": 150,
            "cacodaemon": 400,
            "ghoul": 300,
            "blue_monster": 500,
            "olho": 400
        }
        
        # Carrega a fonte
        self.font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 16)
        
        # Cores
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
    
    def add_points(self, enemy_type):
        """Adiciona pontos baseado no tipo de inimigo"""
        self.score += self.enemy_points.get(enemy_type, 0)
    
    def add_coin(self):
        """Adiciona 50 pontos ao score"""
        self.score += 50
    
    def reset_score(self):
        """Reinicia a pontuação"""
        self.score = 0
    
    def draw(self):
        """Desenha a pontuação na tela"""
        score_text = f"SCORE:{self.score}"
        
        # Posição alinhada com os outros elementos
        base_y = 30
        base_x = 300
        
        # Desenha a sombra do texto
        shadow_surf = self.font.render(score_text, True, self.shadow_color)
        self.window.get_screen().blit(shadow_surf, (base_x + 1, base_y + 1))
        
        # Desenha o texto principal
        text_surf = self.font.render(score_text, True, self.text_color)
        self.window.get_screen().blit(text_surf, (base_x, base_y))
