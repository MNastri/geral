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
    learning_abc()
