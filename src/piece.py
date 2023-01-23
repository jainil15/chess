import os


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value_sign * value
        self.moves = []
        self.moved = False
        self.set_texture()
        self.texure_rect = texture_rect
        
    def set_texture(self, size=64):
        color_intials= 'w'if self.color == 'white' else 'b'
        name_initials = 'K' if self.name == 'king' else 'Q' if self.name == 'queen' else 'R' if self.name == 'rook' else 'B' if self.name == 'bishop' else 'N' if self.name == 'knight' else 'P' if self.name == 'pawn' else ''
        self.texture = os.path.join(f'C:/PDF/chess/assets/piece/alpha/{color_intials}{name_initials}.svg')

        
    def add_move(self, move):
        self.moves.append(move)
        
    def clear_moves(self):
        self.moves = []
            
class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)
        
class Knight(Piece):
    def __init__(self,color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)

class Rook(Piece):
    def __init__(self,color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self,color):
        super().__init__('queen',color, 9.0)
        
class King(Piece):
    def __init__(self,color):
        super().__init__('king',color, 10000.0)