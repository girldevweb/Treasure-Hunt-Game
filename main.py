from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from menus.menu import Menu
from menus.level_select import LevelSelect
from settingsGame.settings import Settings
from screens.credits import Credits
from levels.level1 import Level1
from settingsGame.audio_manager import AudioManager
from screens.intro_scene import IntroScene
import os
from settingsGame.score import ScoreSystem


import pygame
pygame.init()  # Inicializa todos os módulos do Pygame
pygame.display.init()




class Game:


    def __init__(self):
        self.window = Window(900, 600)
        self.window.set_title("Treasure Hunt")
        self.score_system = ScoreSystem(self.window)
        # Estados do jogo
        self.START = 0
        self.MENU = 1
        self.LEVEL_SELECT = 2
        self.SETTINGS = 3
        self.CREDITS = 4
        self.QUIT = 5
        self.run_level1 = 6
        self.INTRO = -1
        self.current_state = self.INTRO
        
        self.running = True
        
        # Cria uma única instância do AudioManager
        self.audio_manager = AudioManager()
        
        # Inicializa apenas os menus primeiro
        self.menu = Menu(self)
        self.level_select = LevelSelect(self)
        self.settings = Settings(self)
        self.credits = Credits(self)
        
        # Level1 será inicializado depois da intro
        self.level1 = None
        
        # Carregando a fonte
        self.font = pygame.font.Font(os.path.join("game/fonts", "PressStart2P.ttf"), 20)
        self.keyboard = self.window.get_keyboard()
        
    def draw_text_centered(self, text, y_pos, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.window.width/2, y_pos))
        self.window.get_screen().blit(text_surface, text_rect)
        
    def run(self):


        while self.running:

            try:
                if self.current_state == self.INTRO:
                    intro = IntroScene(self)
                    action = intro.run()
                    if action:
                        # Inicializa o Level1 depois da intro
                        self.level1 = Level1(self)
                        self.audio_manager.stop_music()
                        self.current_state = self.MENU
                elif self.current_state == self.MENU:
                    self.menu.run()
                elif self.current_state == self.LEVEL_SELECT:
                    self.level_select.run()
                elif self.current_state == self.SETTINGS:
                    self.settings.run()
                elif self.current_state == self.CREDITS:
                    self.credits.run()
                elif self.current_state == self.run_level1:
                    if self.level1:
                        # Define o nível
                        self.audio_manager.set_level(1)
                        # Toca a música explicitamente
                        self.audio_manager.play_music("theme")
                        result = self.level1.run()  # Captura o retorno do nível
                        # Para a música ao sair
                        self.audio_manager.stop_music()
                        
                        # Trata o retorno do nível
                        if result == "level_select" or result == "level2":  # Aceita ambos os retornos
                            self.current_state = self.LEVEL_SELECT
                        elif result == "menu":
                            self.current_state = self.MENU
                elif self.current_state == self.QUIT:
                    self.running = False

                    # Antes de fazer o update final, verifica se o Pygame ainda está ativo
                if pygame.get_init() and pygame.display.get_init():
                    self.window.update()
                else:
                    break

            except pygame.error:
                break  # Sai do loop se houver erro
            except SystemExit:
                break  
                
            
          

           

if __name__ == "__main__":
  
    game = Game()
    game.run()

    pygame.quit()

    