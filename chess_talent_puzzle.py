from abc import (
    ABC,
    abstractmethod,
)
from collections import deque
from pprint import pprint
from sys import intern


class Puzzle(ABC):
    pos = ""
    goal = ""

    def __init__(self, pos=None):
        if pos:
            self.pos = pos

    def __repr__(self):
        return repr(self.pos)

    def isgoal(self):
        return self.pos == self.goal

    def canonical(self):
        return repr(self)

    @abstractmethod
    def __iter__(self):
        if 0:
            yield 0

    def solve(puzzle, depth_first=False, how_many=7):
        solutions = list()
        # queue = deque([puzzle])
        queue = deque()
        trail = {intern(puzzle.canonical()): None}
        add_move = queue.append if depth_first else queue.appendleft
        for ii in range(how_many):
            solution = deque()
            while not puzzle.isgoal():
                moves_to_add = [move for move in puzzle]
                positions = [mv.pos for mv in moves_to_add]
                if -1 in positions:
                    puzzle = queue.pop()
                    continue
                for move in filter(lambda x: x.pos != -1, moves_to_add):
                    canon_representation = move.canonical()
                    if canon_representation in trail:
                        continue
                    trail[intern(canon_representation)] = puzzle
                    add_move(move)
                print(len(queue))
                if len(queue) == 0:
                    break
                puzzle = queue.pop()
            if len(queue) == 0:
                break  # todo handle solved puzzle with empty queue
            while puzzle:
                solution.appendleft(puzzle)
                puzzle = trail[puzzle.canonical()]
            solutions.append(len(solutions) // 2)  # todo
            solutions.append(solution)
            puzzle = queue.pop()
        return solutions


class ChessTalent(Puzzle):
    # new lines    ↓       ↓       ↓       ↓       ↓       ↓       ↓
    pos = "0000000000000000000000000000000000000000pppp0000000000000Q000000"

    def __init__(self, pos=None, whites_turn=True):
        self.whites_turn = whites_turn
        super().__init__(pos)

    def isgoal(self):
        return (
            self.pos.count("p") == 0
            and self.pos.count("q") == 0
            and self.pos.count("Q") == 1
        )

    def __getitem__(self, item):
        return self.pos[item]

    def __repr__(self):
        rows = ["\n"]
        for r in range(8):
            row = self.pos[r * 8 : r * 8 + 8] + "\n"
            rows.append(row)
        return "".join(rows)

    def _make_move(self, piece, mv_from, mv_to):
        if mv_from < mv_to:
            return (
                self[:mv_from]
                + "0"
                + self[mv_from + 1 : mv_to]
                + piece
                + self[mv_to + 1 :]
            )

        return (
            self[:mv_to] + piece + self[mv_to + 1 : mv_from] + "0" + self[mv_from + 1 :]
        )

    def _make_white_moves(self):
        white_queen = self.pos.index("Q")
        white_queen_move = lambda r, c: self._make_move("Q", white_queen, r * 8 + c)
        row, col = divmod(white_queen, 8)
        # print(white_queen, row, col)

        top_limit = -1
        bot_limit = 8
        for r in range(8):
            if self[r * 8 + col] != "0" and self[r * 8 + col] != "Q":
                top_limit = r if r < row else top_limit
                bot_limit = r if r > row and bot_limit == 8 else bot_limit
        for r in range(8):
            if r < top_limit or r > bot_limit or r == row:
                continue
            yield white_queen_move(r, col)

        left_limit = -1
        right_limit = 8
        for c in range(8):
            if self[row * 8 + c] != "0" and self[row * 8 + c] != "Q":
                left_limit = c if c < col else left_limit
                right_limit = c if c > col and right_limit == 8 else right_limit
        for c in range(8):
            if c < left_limit or c > right_limit or c == col:
                continue
            yield white_queen_move(row, c)

        # ascending diagonals
        on_left_side = True if row + col < 8 else False
        diagonal_places = min(row + col, 14 - row - col) + 1
        if on_left_side:
            diagonal = lambda: zip(
                reversed(range(diagonal_places)), range(diagonal_places)
            )
        else:
            diagonal = lambda: zip(
                reversed(range(8 - diagonal_places, 8)), range(8 - diagonal_places, 8)
            )
        top_limit = -1
        bot_limit = 8
        for r, c in diagonal():
            if self[r * 8 + c] != "0" and self[r * 8 + c] != "Q":
                top_limit = r if r < row and top_limit == -1 else top_limit
                bot_limit = r if r > row else bot_limit
        for r, c in diagonal():
            if r < top_limit or r > bot_limit or r == row:
                continue
            yield white_queen_move(r, c)

        # descending diagonals
        on_left_side = True if col - row < 1 else False
        diagonal_places = min(7 - row + col, 7 + row - col) + 1
        if on_left_side:
            diagonal = lambda: zip(
                range(8 - diagonal_places, 8), range(diagonal_places)
            )
        else:
            diagonal = lambda: zip(
                range(diagonal_places), range(8 - diagonal_places, 8)
            )
        top_limit = -1
        bot_limit = 8
        for r, c in diagonal():
            if self[r * 8 + c] != "0" and self[r * 8 + c] != "Q":
                top_limit = r if r < row else top_limit
                bot_limit = r if r > row and bot_limit == 8 else bot_limit
        for r, c in diagonal():
            if r < top_limit or r > bot_limit or r == row:
                continue
            yield white_queen_move(r, c)

    def _make_black_moves(self):
        black_pieces = [
            idx for idx, piece in enumerate(self.pos) if piece in {"p", "q"}
        ]
        # pprint(black_pieces)
        for bp in black_pieces:
            row, col = divmod(bp, 8)
            if self[bp] == "q":
                yield -1
            if self[bp] == "p":
                piece = "q" if row == 6 else "p"
                if self[bp + 8] != "Q":
                    yield self._make_move(piece, bp, bp + 8)
                if col > 0 and self[bp + 7] == "Q":
                    yield -1
                if col < 7 and self[bp + 9] == "Q":
                    yield -1

    def __iter__(self):
        if self.whites_turn:
            for pos in self._make_white_moves():
                # print(pos)
                yield ChessTalent(pos, False)
        else:
            for pos in self._make_black_moves():
                # print(pos)
                yield ChessTalent(pos)


pprint(ChessTalent().solve(True, 100))
