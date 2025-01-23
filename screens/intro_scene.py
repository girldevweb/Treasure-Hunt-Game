import pygame
import math
from settingsGame.settings_game import *
import os

class IntroScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.window.get_screen()
        self.width = GameSettings["WINDOW_WIDTH"]
        self.height = GameSettings["WINDOW_HEIGHT"]
       
        # Para qualquer música que esteja tocando antes de iniciar a intro
        self.game.audio_manager._last_played_music = None
        self.game.audio_manager.stop_music()
        pygame.time.wait(100)  # Pequena pausa para garantir que a música anterior parou
        
       
        # Cores
        self.parchment_color = (250, 240, 230)
        self.text_color = (70, 40, 10)
        self.title_color = (139, 69, 19)
       
        # Carrega fontes
        self.title_font = pygame.font.Font(os.path.join("game/fonts", "MedievalSharp.ttf"), 48)
        self.text_font = pygame.font.Font(os.path.join("game/fonts", "MedievalSharp.ttf"), 24)
       
        # Som
        self.type_sound = pygame.mixer.Sound(os.path.join("game/sounds", "type.wav"))
        self.type_sound.set_volume(0.05)
        self.page_turn = pygame.mixer.Sound(os.path.join("game/sounds", "page_turn.mp3"))
        self.page_turn.set_volume(0.3)
       
        # Estado inicial
        self.current_page = 0
        self.char_index = 0
        self.text_delay = 30
        self.sound_delay = 50
        self.last_char_time = pygame.time.get_ticks()
        self.last_sound_time = pygame.time.get_ticks()
        self.is_typing = False
       
        # Adiciona variáveis para animação da chave
        self.key_frames = []
        self.key_frame_index = 0
        self.last_key_update = pygame.time.get_ticks()
        self.key_animation_delay = 100
        
        # Variáveis para animação do player
        self.player_frames = []
        self.player_frame_index = 0
        self.last_player_update = pygame.time.get_ticks()
        self.player_animation_delay = 150  # Ajuste esse valor para controlar a velocidade
       
        # Carrega imagens e configura história
        self.load_images()
        self.setup_story()
        
        # Inicia a música da intro
        self.game.audio_manager.play_music("intro")

    def load_images(self):
        # Carrega a folha de pergaminho
        self.book = pygame.image.load(Items["folha"]).convert_alpha()
        
        # Ajusta a escala para cobrir toda a janela
        scale_x = self.width / self.book.get_width()
        scale_y = self.height / self.book.get_height()
        scale = max(scale_x, scale_y)  # Usa o maior valor para garantir cobertura total
        
        new_width = int(self.book.get_width() * scale)
        new_height = int(self.book.get_height() * scale)
        
        self.book = pygame.transform.scale(self.book, (new_width, new_height))
        
        # Carrega a spritesheet da chave e extrai os frames
        key_sheet = pygame.image.load(Items["key"]).convert_alpha()
        key_scale = 1.5
        frame_width = 32
        frame_height = 32
        
        # Extrai os 8 frames da spritesheet
        for i in range(8):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(key_sheet, (0, 0), frame_rect)
            frame = pygame.transform.scale(frame, 
                (int(frame_width * key_scale), int(frame_height * key_scale)))
            self.key_frames.append(frame)
        
        # Carrega os frames do player
        sprite_scale = 2.0
        for sprite_path in Player_Sprites["idle"]:
            frame = pygame.image.load(sprite_path).convert_alpha()
            frame = pygame.transform.scale(frame, 
                (int(48 * sprite_scale), int(48 * sprite_scale)))
            self.player_frames.append(frame)
        
        # Carrega outros sprites
        self.story_images = {
            'player': self.player_frames[0],  # Inicialmente usa o primeiro frame
            'chest': pygame.transform.scale(
                pygame.image.load(Items["bau_locked"]).convert_alpha(),
                (32 * sprite_scale, 32 * sprite_scale)
            ),
            'key': self.key_frames[0],
            'boss': pygame.transform.scale(
                pygame.image.load(Final_Boss["boss"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            )
        }

    def setup_story(self):
        # Carrega alguns inimigos para a história
        sprite_scale = 2.0
        enemy_images = {
            'bat': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["bat"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            ),
            'ghoul': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["ghoul"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            ),
            'minotaur': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["minotaur"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            ),
            'olho': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["olho"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            ),
            'cacodaemon': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["cacodaemon"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            ),
            'blue_monster': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["blue_monster"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            ),
            'brain': pygame.transform.scale(
                pygame.image.load(Enemy_Sprites["brain"]["walk"][0]).convert_alpha(),
                (48 * sprite_scale, 48 * sprite_scale)
            )

        }
        
        # Adiciona os inimigos ao dicionário de imagens
        self.story_images.update(enemy_images)
        
        # Páginas da história atualizadas
        self.story_pages = [
            {
                "text": "Nas profundezas de uma antiga floresta,\numa lenda sussurra sobre um tesouro lendário...",
                "image": 'chest'
            },
            {
                "text": "Veena, uma destemida caçadora de tesouros,\nembarca em uma jornada perigosa afim de\ndesvendar a lenda...",
                "image": 'player'
            },
            {
                "text": "O caminho é guardado por criaturas místicas\nque espreitam nas sombras...",
                "images": ['olho', 'cacodaemon', 'blue_monster', 'brain'],
                "image_spacing": 100 
            },
            {
                "text": "Ghouls que emergem das profundezas\nE ferozes minotauros que protegem\nos segredos da floresta...",
                "images": ['ghoul', 'minotaur'],
                "image_spacing": 100  # Espaço entre as imagens
            },
            {
                "text": "No coração da floresta, um poderoso guardião\nprotege o tesouro com sua vida\nApenas os mais corajosos ousam enfrentá-lo...",
                "image": 'boss'
            },
            {
                "text": "Uma antiga chave mágica é necessária\npara desbloquear o tesouro guardado\nnas profundezas da floresta...",
                "image": 'key'
            },
            {
                "text": "TREASURE HUNT\n\n\n\nVocê está pronto para essa\njornada em busca do tesouro?",
                "image": None
            }
        ]

    def draw(self):
        # Fundo escuro
        self.screen.fill((20, 20, 20))
        
        # Centraliza a folha
        parchment_x = (self.width - self.book.get_width()) // 2
        parchment_y = (self.height - self.book.get_height()) // 2
        self.screen.blit(self.book, (parchment_x, parchment_y))
        
        # Obtém a página atual
        page = self.story_pages[self.current_page]
        
        # Efeito de digitação
        now = pygame.time.get_ticks()
        if self.char_index < len(page["text"]):
            if now - self.last_char_time > self.text_delay:
                self.char_index += 1
                self.last_char_time = now
                
                if (self.char_index > 0 and
                    page["text"][self.char_index-1] not in [' ', '\n'] and
                    now - self.last_sound_time > self.sound_delay):
                    self.type_sound.play()
                    self.last_sound_time = now
                    self.is_typing = True
        else:
            self.is_typing = False
        
        # Divide o texto em linhas e desenha
        text = page["text"][:self.char_index]
        lines = text.split('\n')
        
        # Área útil do pergaminho (removendo margens)
        usable_width = self.book.get_width() * 0.7  # 70% da largura do pergaminho
        text_start_y = parchment_y + self.book.get_height() * 0.2
        
        # Desenha cada linha centralizada
        text_y = text_start_y
        for line in lines:
            if "TREASURE HUNT" in line:
                text_surface = self.title_font.render(line, True, self.title_color)
            else:
                text_surface = self.text_font.render(line, True, self.text_color)
            
            # Calcula a posição x para centralizar o texto
            text_x = parchment_x + (self.book.get_width() - text_surface.get_width()) // 2
            self.screen.blit(text_surface, (text_x, text_y))
            text_y += 35
        
        # Atualiza animações
        current_time = pygame.time.get_ticks()
        
        # Atualiza frame da chave
        if current_time - self.last_key_update > self.key_animation_delay:
            self.key_frame_index = (self.key_frame_index + 1) % len(self.key_frames)
            self.story_images['key'] = self.key_frames[self.key_frame_index]
            self.last_key_update = current_time
        
        # Atualiza frame do player
        if current_time - self.last_player_update > self.player_animation_delay:
            self.player_frame_index = (self.player_frame_index + 1) % len(self.player_frames)
            self.story_images['player'] = self.player_frames[self.player_frame_index]
            self.last_player_update = current_time
        
        # Desenha a imagem se houver
        if page.get("image") or page.get("images"):
            if page.get("image"):
                # Desenha uma única imagem
                image = self.story_images[page["image"]]
                image_x = parchment_x + (self.book.get_width() - image.get_width()) // 2
                image_y = text_y + 20 + math.sin(pygame.time.get_ticks() * 0.003) * 5
                self.screen.blit(image, (image_x, image_y))
            elif page.get("images"):
                # Desenha múltiplas imagens lado a lado
                total_width = sum([self.story_images[img].get_width() for img in page["images"]])
                total_width += (len(page["images"]) - 1) * page["image_spacing"]
                
                start_x = parchment_x + (self.book.get_width() - total_width) // 2
                for i, img_name in enumerate(page["images"]):
                    image = self.story_images[img_name]
                    image_x = start_x + i * (image.get_width() + page["image_spacing"])
                    image_y = text_y + 20 + math.sin(pygame.time.get_ticks() * 0.003) * 5
                    self.screen.blit(image, (image_x, image_y))
        
        # Instrução para continuar (mantida centralizada)
        if self.char_index >= len(page["text"]):
            continue_text = self.text_font.render("Pressione ENTER para continuar...",
                                                True, self.text_color)
            continue_x = parchment_x + (self.book.get_width() - continue_text.get_width()) // 2
            continue_y = parchment_y + self.book.get_height() - 60
            self.screen.blit(continue_text, (continue_x, continue_y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Se ainda está digitando
                    if self.char_index < len(self.story_pages[self.current_page]["text"]):
                        self.char_index = len(self.story_pages[self.current_page]["text"])
                    # Se já terminou de digitar
                    else:
                        # Se não é a última página
                        if self.current_page < len(self.story_pages) - 1:
                            self.current_page += 1
                            self.char_index = 0
                            self.page_turn.play()
                        # Se é a última página
                        else:
                            self.game.intro_completed = True
                            self.game.current_state = self.game.MENU
                            # Para a música antes de sair da intro
                            self.game.audio_manager.stop_music()
                            pygame.time.wait(300)
                            return "exit_intro"
                           
                elif event.key == pygame.K_ESCAPE:
                    self.game.intro_completed = True
                    self.game.current_state = self.game.MENU
                    # Para a música ao sair com ESC
                    self.game.audio_manager.stop_music()
                    return "exit_intro"
        return None

    def run(self):
        clock = pygame.time.Clock()
       
        while True:
            clock.tick(60)
           
            action = self.handle_events()
            if action == "exit_intro":
                return True  # Retorna True para indicar que deve ir para o menu
            elif action == "quit":
                self.game.window.close()
                return False
           
            self.draw()
            pygame.display.flip()
