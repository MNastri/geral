import os
import sqlite3


def learning_abc():
    from abc import (
        ABC,
        abstractmethod,
    )

    class Entertainer(ABC):
        @abstractmethod
        def sing(self, song):
            pass

        @abstractmethod
        def dance(self):
            pass

        def all_the_other_stuff(self, msg):
            print(msg)

    print("The abstract methods of Entertainer are:", Entertainer.__abstractmethods__)

    class StreetPerformer(Entertainer):
        def sing(self, song):
            return f"Loud version of {song}"

        def dance(self):
            return f"Bold break dance"

    print(
        "StreetPerformer is an Entertainer?", issubclass(StreetPerformer, Entertainer)
    )
    print("Instance of StreetPerformer created. sp =", sp := StreetPerformer())
    print("Is sp an instance of StreetPerformer?", isinstance(sp, StreetPerformer))
    print("Is sp an instance of Entertainer?", isinstance(sp, StreetPerformer))
    msg = """\nBy subclassing Entertainer in StreetPerformer we added all the
attributes from the Entertainer to the StreetPerformer. We implemented sing and 
dance in StreetPerformer to override the ones in the base class, but we did not 
implement all_the_other_stuff in StreetPerformer and we will get it for free.
This means that subclassing can alter our class with the base class' attributes.
We did not decorate all_the_other_stuff with abstractmethod or it would raise a
TypeError at run time because all the decorated methods in the base class need 
also to be defined in their subclasses.\n\n"""
    StreetPerformer().all_the_other_stuff(msg=msg)

    class LoungePerformer:
        def sing(self, song):
            return f"Soft version of {song}"

        def dance(self):
            return f"Gentle moody dance"

    Entertainer.register(LoungePerformer)
    print(
        "LoungePerformer is an Entertainer?", issubclass(StreetPerformer, Entertainer)
    )
    print("Instance of LoungePerformer created. lp =", lp := LoungePerformer())
    print("Is lp an instance of LoungePerformer?", isinstance(lp, LoungePerformer))
    print("Is lp an instance of Entertainer?", isinstance(lp, Entertainer))
    print(
        "is all_the_other_stuff in LoungePerformer?",
        "all_the_other_stuff" in dir(LoungePerformer),
    )
    msg1 = """\nBy registering LoungPerformer as an Entertainer we can overload the 
isinstance and issubclass functions to return True when checking if our class is
an instance/subclass from the base class. This will be useful if we do not want 
to add any attributes from the base class into our class. The abstractmethod
decorator will not affect a registered subclass and will not raise any error.
But the missing method will fail at runtime.\n\n"""
    print(msg1)

    class HobbyistPerformer:
        def sing(self, song):
            return f"Faulty version of {song}"

        def dance(self):
            return f"Clumsy dance"

    print(
        "HobbyistPerformer can sing and can dance?",
        {"sing", "dance"}.issubset(set(dir(HobbyistPerformer))),
    )
    print(
        "HobbyistPerformer is an Entertainer?",
        issubclass(HobbyistPerformer, Entertainer),
    )
    print("Instance of LoungePerformer created. hp =", hp := HobbyistPerformer())
    print("Is hp an instance of HobbyistPerformer?", isinstance(hp, HobbyistPerformer))
    print("Is hp an instance of Entertainer?", isinstance(hp, Entertainer))
    msg2 = """\nABC does not try to recognize if our class is a subclass of a 
base class. They can only do that through subclassing or registration."""


def learn_framework_design_pattern():
    """The parent class provides an engine that calls methods in a subclass. Those
    required methods are listed as being abstract.

    Usually, the parent manages the execution flow and the subclass provides the
    details"""
    import re

    from abc import (
        ABC,
        abstractmethod,
    )
    from collections import deque
    from sys import intern

    class Puzzle(ABC):
        pos = ""
        goal = ""

        def __init__(self, pos=None):
            if pos:
                self.pos = pos

        def __repr__(self):
            return repr(self.pos)

        def canonical(self):
            return repr(self)

        def isgoal(self):
            return self.pos == self.goal

        @abstractmethod
        def __iter__(self):
            if 0:
                yield self

        def solve(puzzle, depth_first=False):
            queue = deque([puzzle])
            trail = {intern(puzzle.canonical()): None}
            solution = deque()
            append_to_queue = queue.append if depth_first else queue.appendleft
            while not puzzle.isgoal():
                for state in puzzle:
                    canon_representation = state.canonical()
                    if canon_representation in trail:
                        continue
                    trail[intern(canon_representation)] = puzzle
                    append_to_queue(state)
                puzzle = queue.pop()
            while puzzle:
                solution.appendleft(puzzle)
                puzzle = trail[puzzle.canonical()]
            return list(solution)

    class Stepper(Puzzle):
        pos = (1, 0, 0, 0, 0, 0)
        goal = (0, 0, 0, 0, 0, 1)

        def __iter__(self):
            i = self.pos.index(1)
            if i > 0:
                yield Stepper((0,) * (i - 1) + (1,) + (0,) * (6 - i))
            if i < 6:
                yield Stepper((0,) * (i + 1) + (1,) + (0,) * (4 - i))

    from pprint import pprint

    pprint(Stepper().solve())

    class JugPuzzle(Puzzle):
        """Given two empty jugs with 3 and 5 liter capacites and a full jug
        with 8 litters, find a sequence of pours leaving four liters in the two
        largest jugs."""

        pos = (0, 0, 8)
        goal = (0, 4, 4)
        capacity = (3, 5, 8)

        def __iter__(self):
            for first_jug_num in range(len(self.pos)):
                for second_jug_num in range(len(self.pos)):
                    if first_jug_num == second_jug_num:
                        continue
                    qty_to_pour = min(
                        self.pos[first_jug_num],
                        self.capacity[second_jug_num] - self.pos[second_jug_num],
                    )
                    if not qty_to_pour:
                        continue
                    duplicate = list(self.pos)
                    duplicate[first_jug_num] -= qty_to_pour
                    duplicate[second_jug_num] += qty_to_pour
                    yield JugPuzzle(tuple(duplicate))

    pprint(JugPuzzle().solve())

    class EightQueens(Puzzle):
        """Place 8 queens on a chess board such that no two queens attack each
        other.
        """

        pos = ()

        def isgoal(self):
            return len(self.pos) == 8

        def __iter__(self):
            xx = len(self.pos)
            for yy in range(8):
                if yy in self.pos:
                    continue
                for x_possibility in range(xx):
                    y_possibility = self.pos[x_possibility]
                    if abs(xx - x_possibility) == abs(yy - y_possibility):
                        break
                else:
                    yield EightQueens(self.pos + (yy,))

        def __repr__(self):
            rows = ["\n"]
            for (
                ii,
                yy,
            ) in enumerate(self.pos):
                row = (["_", "."] if ii & 1 else [".", "_"]) * 4 + ["\n"]
                row[yy] = "Q"
                rows.append("".join(row))
            return "".join(rows)

    pprint(EightQueens().solve())

    class TriPuzzle(Puzzle):
        """http://www.pegsgame.com/types-of-pegs-game/cracker-barrel-peg-game.html"""

        pos = "011111111111111"
        goal = "100000000000000"
        # triples = positions where we might be able to make a jump
        triplets = [
            (0, 1, 3),
            (1, 3, 6),
            (3, 6, 10),
            (2, 4, 7),
            (4, 7, 11),
            (5, 8, 12),
            (0, 2, 5),
            (2, 5, 9),
            (5, 9, 14),
            (1, 4, 8),
            (4, 8, 13),
            (3, 7, 12),
            (10, 11, 12),
            (11, 12, 13),
            (12, 13, 14),
            (6, 7, 8),
            (7, 8, 9),
            (3, 4, 5),
        ]

        def __iter__(self):
            for tt in self.triplets:
                if (
                    self.pos[tt[0]] == "1"
                    and self.pos[tt[1]] == "1"
                    and self.pos[tt[2]] == "0"
                ):
                    yield TriPuzzle(self.produce(tt, "001"))
                if (
                    self.pos[tt[0]] == "0"
                    and self.pos[tt[1]] == "1"
                    and self.pos[tt[2]] == "1"
                ):
                    yield TriPuzzle(self.produce(tt, "100"))

        def produce(self, triplet, new_value):
            t0, t1, t2 = triplet
            v0, v1, v2 = new_value
            return (
                self.pos[:t0]
                + v0
                + self.pos[t0 + 1 : t1]
                + v1
                + self.pos[t1 + 1 : t2]
                + v2
                + self.pos[t2 + 1 :]
            )

        def canonical(self):
            """reflects self.pos and returns the "biggest" from the two.
            example
            "100000000000000" > "010000000000000"
            "010000000000000" > "001000000000000" NOTE: these are reflections
            "000100000000000" > "000001000000000" NOTE: these are reflections
            """
            pp = self.pos
            qq = "".join(
                map(pp.__getitem__, (0, 2, 1, 5, 4, 3, 9, 8, 7, 6, 14, 13, 12, 11, 10))
            )
            return max(pp, qq)

        def __repr__(self):
            rows = ["\n"]
            for ii in range(5):
                start = int(ii * (ii + 1) / 2)
                end = int((ii + 2) * (ii + 1) / 2)
                pos = [" {}".format(cc) for cc in self.pos[start:end]]
                qty_charact = (end - start) * 2
                qty_blanks = int((15 - qty_charact) / 2)
                row = [" "] * qty_blanks + pos + [" "] * qty_blanks + ["\n"]
                rows.append("".join(row))
            return "".join(rows)

    pprint(TriPuzzle().solve())


def main():
    database = "teste.sqlite3"
    con = sqlite3.connect(database)
    cur = con.cursor()
    tables = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    if not tables:
        cur.execute("CREATE TABLE tb_teste (date text, qty real);")
        con.commit()
        cur.execute("""INSERT INTO  tb_teste VALUES ('test',199);""")
        con.commit()
    for table in tables:
        query = cur.execute("""SELECT * FROM '{}';""".format(table[0]))
        for row in query:
            print(row)
    con.close()


if __name__ == "__main__":
    # main()
    # learning_abc()
    learn_framework_design_pattern()
