from random import choice

import numpy
import pygame

BOARD_X = 10
BOARD_Y = 20

PIECE_WIDTH = 20

BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class Piece:

    def __init__(self, template, color):
        self.color = color
        self.template = numpy.array(template)
        self.height = self.template.shape[0]
        self.width = self.template.shape[1]

    def rotate_left(self):
        self.template = numpy.rot90(self.template)
        self.height = self.template.shape[0]
        self.width = self.template.shape[1]

    def rotate_right(self):
        self.template = numpy.rot90(self.template, -1)
        self.height = self.template.shape[0]
        self.width = self.template.shape[1]

    def display(self, screen, offset):
        for x in range(len(self.template)):
            for y in range(len(self.template[x])):
                if self.template[x][y] == 1:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        pygame.Rect(
                            y * PIECE_WIDTH + offset[1] * PIECE_WIDTH,
                            x * PIECE_WIDTH + offset[0] * PIECE_WIDTH,
                            PIECE_WIDTH,
                            PIECE_WIDTH
                        )
                    )


class Square(Piece):
    template = [
        [1, 1],
        [1, 1]
    ]

    color = "purple"

    def __init__(self):
        super().__init__(self.template, self.color)


class Line(Piece):
    template = [
        [1, 1, 1, 1]
    ]

    color = "red"

    def __init__(self):
        super().__init__(self.template, self.color)


class LeftL(Piece):
    template = [
        [1, 0, 0],
        [1, 1, 1]
    ]

    color = "orange"

    def __init__(self):
        super().__init__(self.template, self.color)


class RightL(Piece):
    template = [
        [0, 0, 1],
        [1, 1, 1]
    ]

    color = "gray"

    def __init__(self):
        super().__init__(self.template, self.color)


class SemiCross(Piece):
    template = [
        [0, 1, 0],
        [1, 1, 1]
    ]

    color = "yellow"

    def __init__(self):
        super().__init__(self.template, self.color)


class Game:
    piece_stack = [Square, LeftL, RightL, SemiCross, Line]

    current_piece = None
    current_piece_offset = [0, 0]

    def __init__(self, board):
        self.last_move = 0
        self.board = board
        self.new_piece()

        pygame.time.get_ticks()

    def new_piece(self):
        self.current_piece_offset = [0, 0]
        piece = choice(self.piece_stack)
        self.current_piece = piece()

    def tick(self):
        if self.piece_will_collide():
            self.save_piece()
            self.check_full_lines()
            self.new_piece()
        else:
            if self.should_fall():
                self.fall()

    def display(self, screen):
        self.board.display(screen)
        self.current_piece.display(screen, self.current_piece_offset)

    def fall(self):
        self.current_piece_offset[0] += 1

    def rotate_left(self):
        if not self.board.will_collide_on_rotation(self.current_piece, self.current_piece_offset):
            self.current_piece.rotate_left()

    def rotate_right(self):
        if not self.board.will_collide_on_rotation(self.current_piece, self.current_piece_offset):
            self.current_piece.rotate_right()

    def piece_will_collide(self):
        # out of lower bound?
        if self.current_piece_offset[0] + self.current_piece.height >= BOARD_Y:
            return True
        # occupied by another piece?
        if self.board.will_collide(self.current_piece, self.current_piece_offset):
            return True

        return False

    def check_full_lines(self):
        self.board.clean_full_lines()

    def should_fall(self):
        if pygame.time.get_ticks() - self.last_move > 480:
            self.last_move = pygame.time.get_ticks()
            return True
        return False

    def move_right(self):
        # Lateral piece collision?
        if self.board.will_collide_right(self.current_piece, self.current_piece_offset):
            return

        # Board limits
        if self.current_piece_offset[1] + 1 + self.current_piece.width < BOARD_X:
            self.current_piece_offset[1] += 1
        else:
            self.current_piece_offset[1] = BOARD_X - self.current_piece.width

    def move_left(self):
        # Lateral piece collision?
        if self.board.will_collide_left(self.current_piece, self.current_piece_offset):
            return

        # Board limits
        if self.current_piece_offset[1] - 1 >= 0:
            self.current_piece_offset[1] -= 1
        else:
            self.current_piece_offset[1] = 0

    def save_piece(self):
        self.board.consolidate(self.current_piece, self.current_piece_offset)


class Board:
    board = BOARD

    def consolidate(self, piece, offset):
        for x in range(len(piece.template)):
            for y in range(len(piece.template[x])):
                if piece.template[x][y] == 1:
                    self.board[offset[0] + x][offset[1] + y] = piece.template[x][y]

    def will_collide(self, piece, offset):
        for x in range(len(piece.template)):
            for y in range(len(piece.template[x])):
                if piece.template[x][y] == 1:
                    if self.board[offset[0] + x + 1][offset[1] + y] == 1:
                        return True

    def will_collide_right(self, piece, offset):
        for x in range(len(piece.template)):
            for y in range(len(piece.template[x])):
                if piece.template[x][y] == 1:
                    # Ensure whe are checking an inside board position
                    if offset[1] + y + 1 < BOARD_X:
                        if self.board[offset[0] + x][offset[1] + y + 1] == 1:
                            return True

    def will_collide_left(self, piece, offset):
        for x in range(len(piece.template)):
            for y in range(len(piece.template[x])):
                if piece.template[x][y] == 1:
                    # Ensure whe are checking an inside board position
                    if offset[1] + y + 1 < BOARD_X:
                        if self.board[offset[0] + x][offset[1] + y - 1] == 1:
                            return True

    def will_collide_on_rotation(self, piece, offset):
        template = numpy.rot90(numpy.array(piece.template))

        for x in range(len(template)):
            for y in range(len(template[x])):
                if template[x][y] == 1:
                    # Going out right bound
                    if offset[1] + y + 1 >= BOARD_X:
                        return True
                    # Collide with piece at right
                    if template[x][y] == 1:
                        if self.board[offset[0] + x][offset[1] + y + 1] == 1:
                            return True

                    # Collide with piece at left
                    if template[x][y] == 1:
                        if self.board[offset[0] + x][offset[1] + y - 1] == 1:
                            return True

    def clean_full_lines(self):
        remove_lines = []
        for y in range(BOARD_Y):
            if numpy.sum(self.board[y]) == 10:
                remove_lines.append(y)
                self.board[y] = [0 for i in range(BOARD_X)]

        for line in remove_lines:
            del self.board[line]

        for _ in remove_lines:
            self.board.insert(0, [0 for _ in range(BOARD_X)])

    def display(self, screen):
        for y in range(BOARD_Y):
            for x in range(BOARD_X):
                pygame.draw.rect(
                    screen,
                    "white" if self.board[y][x] != 1 else 'purple',
                    pygame.Rect(x * PIECE_WIDTH, y * PIECE_WIDTH, PIECE_WIDTH, PIECE_WIDTH)
                )


def game():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    board = Board()
    _game = Game(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            _game.move_left()
        if keys[pygame.K_d]:
            _game.move_right()
        if keys[pygame.K_w]:
            _game.rotate_left()
        if keys[pygame.K_s]:
            _game.rotate_right()

        screen.fill("black")

        _game.tick()
        _game.display(screen)

        pygame.display.flip()

        clock.tick(30)


if __name__ == '__main__':
    game()
