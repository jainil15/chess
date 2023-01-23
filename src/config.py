import pygame 
import os

from sound import Sound
from theme import Theme

class Config:
    
    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        #font
        self.font = pygame.font.SysFont('Consolas', 18, bold=True)
        self.uifont = pygame.font.SysFont('Rubik', 28, bold=True)
        #sound
        self.move_sound = Sound(
            os.path.join('assets/sound/standard/Move1.mp3')
        )
        self.capture_sound = Sound(
            os.path.join('assets/sound/standard/Capture1.mp3')
        )
        self.check_sound = Sound(
            os.path.join('assets/sound/standard/Check1.mp3')
        )
    
    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]
        
            
    def _add_themes(self):
        green = Theme( (234, 235, 200), (119,154,88),(244,247,116), (172,195,51), '#f07470','#ea4c46' )
        brown = Theme( (235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#d3d3d3', '#9e9e9e' )
        blue = Theme( (229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#d3d3d3', '#9e9e9e' )
        gray = Theme( (120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#d3d3d3', '#9e9e9e' )
        
        self.themes = [green,brown,blue,gray]