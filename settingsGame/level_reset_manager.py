import pygame
from settingsGame.door import Door  # Importa a classe Door
from settingsGame.settings_game import world_data1, world_data2

class LevelResetManager:
    def __init__(self, game):
        self.game = game

    def reset_level(self, level):
        """Reseta o nível para seu estado inicial"""
        # Reseta estados básicos do nível
        level.player_health = 3
        level.show_game_over = False
        level.is_paused = False
        level.game_over_screen = None
        

            # Reseta a posição do player para a posição inicial
        level.player.rect.x = 100  # Posição inicial X
        level.player.rect.y = level.window.height - 130  # Posição inicial Y
        level.player.velocity_y = 0  # Reseta a velocidade vertical
        level.player.velocity_x = 0  # Reseta a velocidade horizontal
        level.player.direction = 1  # Reseta a direção (1 = direita)
        if hasattr(level.player, 'shield_active'):
            level.player.shield_active = False  # Reseta o escudo se existir
        # Reseta coletáveis
        level.coins = 0
        level.potions = 0
        level.keys = 0
        
        # Reseta grupos de sprites
        level.enemy_group.empty()
        level.coins_group.empty()
        level.potions_group.empty()
        level.keys_group.empty()
          # Limpa o grupo de traps apenas se existir (Level3)
        if hasattr(level, 'traps_group'):
            level.traps_group.empty()
        
        # Reseta grupos específicos do nível
        if hasattr(level, 'boss_group'):
            level.boss_group.empty()
        if hasattr(level, 'treasure_group'):  # Adiciona verificação para treasure_group
            level.treasure_group.empty()
        if hasattr(level, 'doors_group'):
            level.doors_group.empty()
            level.doors_group = pygame.sprite.Group()  # Recria o grupo
        
            # Determina qual world_data usar
            if isinstance(level, self.game.level1.__class__):
                world_data = world_data1
            else:
                world_data = world_data2
                
            # Cria a porta na posição correta
            for y, row in enumerate(world_data):
                for x, tile in enumerate(row):
                    if tile == "D":
                        door = Door(x * level.tile_size, y * level.tile_size)
                        level.doors_group.add(door)
            
            
        # Recria o mundo
        level.create_world()
        
        # Recria os inimigos e coletáveis
        level.create_enemies()
        level.create_collectibles()
        
        # Recria o boss apenas se o nível tiver esse método
        if hasattr(level, 'create_boss'):
            level.create_boss()
        
        # Reseta o sistema de pontuação
        level.score_system.reset_score()
        
        # Atualiza o display de coletáveis
        level.collectibles_display.update_counts(coins=0, keys=0, potions=0)
        
        return level
