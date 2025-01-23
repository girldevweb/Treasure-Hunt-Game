import pygame
from settingsGame.settings_game import Sounds
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        
        # Carrega as configurações salvas
        self.load_settings()
        
        self._in_intro = False
        self._is_muted = False
        self._previous_volume = self._volume
        self._current_music = None
        self._is_playing = False
        self._last_played_music = None
        self._current_level = 1
        
        # Carrega a música tema e efeitos
        self.theme = pygame.mixer.Sound(os.path.join("game/sounds", "forest.wav"))
        self.theme2 = pygame.mixer.Sound(os.path.join("game/sounds", "cave.wav"))
        self.theme3 = pygame.mixer.Sound(os.path.join("game/sounds", "finale.wav"))
        self.intro_music = pygame.mixer.Sound(os.path.join("game/sounds", "intro_music.mp3"))
        
        self.effects = {
            "attack": pygame.mixer.Sound(Sounds["attack"]),
            "click": pygame.mixer.Sound(Sounds["click"]),
            "collect": pygame.mixer.Sound(Sounds["collect"]),
            "hit": pygame.mixer.Sound(Sounds["hit"]),
            "jump": pygame.mixer.Sound(Sounds["jump"])
        }
        
        # Aplica volume inicial
        self._apply_volume()
    
    def load_settings(self):
        """Carrega as configurações de áudio salvas"""
        try:
            with open("game/settings.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.strip().split("=")
                    if key == "volume":
                        self._volume = float(value) / 100.0
                    elif key == "bgm":
                        self._is_muted = not bool(int(value))
        except:
            # Valores padrão se não houver arquivo de configurações
            self._volume = 1.0
            self._is_muted = False
    
    def _apply_volume(self):
        """Aplica o volume atual a todos os sons"""
        volume = 0 if self._is_muted else self._volume
        
        self.theme.set_volume(volume * 0.3)
        self.theme2.set_volume(volume * 0.3)
        self.theme3.set_volume(volume * 0.3)
        self.intro_music.set_volume(volume * 0.3)
        
        for effect in self.effects.values():
            effect.set_volume(volume)
    
    def set_level(self, level):
        """Define o nível atual e atualiza a música"""
        if self._in_intro:  # Não muda música se estiver na intro
            return
       
        self._current_level = level
        
        # Define a música correta para o nível
        music_name = f"theme{level if level > 1 else ''}"
       
        # Atualiza e toca a música
        self._last_played_music = music_name
    
    def play_music(self, music_name):
        """Toca uma música específica"""
        
        
        if music_name == "intro":
            self._in_intro = True
            
        # Guarda a música atual
        self._last_played_music = music_name
    
        
        if self._is_muted:
           
            return
        
        # Se já estiver tocando a mesma música, não faz nada
        if self._current_music == music_name and self._is_playing:
            return
        
        # Para qualquer música que esteja tocando
        self.stop_music()
        
     
        if music_name == "theme":
            self.theme.play(-1)
        elif music_name == "theme2":
            self.theme2.play(-1)
        elif music_name == "theme3":
            self.theme3.play(-1)
        elif music_name == "intro":
            self.intro_music.play(-1)
        
        self._current_music = music_name
        self._is_playing = True
    
    
    def resume_music(self):
        """Retoma a última música tocada"""
      
        
        if self._last_played_music:
          
            self.play_music(self._last_played_music)
     
    
    def stop_music(self):
        """Para a música atual"""
        pygame.mixer.stop()
        self._is_playing = False
        if self._current_music == "intro":
            self._in_intro = False
        self._current_music = None
    
    def play_effect(self, effect_name):
        """Toca um efeito sonoro"""
        if not self._is_muted and effect_name in self.effects:
            self.effects[effect_name].play()
    
    def toggle_mute(self):
        """Alterna entre mudo/desmudo"""
       
        
        self._is_muted = not self._is_muted
        
        if self._is_muted:
           
            self.stop_music()
        else:
          
            music_name = f"theme{self._current_level if self._current_level > 1 else ''}"
            
            self.play_music(music_name)
        
        self._apply_volume()
      
    
    @property
    def is_muted(self):
        return self._is_muted
    
    def cleanup(self):
        self.stop_music()
    
    # Métodos para integração com Settings
    def set_volume(self, volume):
        """Ajusta o volume (0-100)"""
        self._volume = volume / 100.0
        self._apply_volume()
    
    def toggle_bgm(self, enabled):
        """Liga/desliga a música de fundo"""
        self._is_muted = not enabled
        if self._is_muted:
            self.stop_music()
        else:
            self.resume_music()
        self._apply_volume()
