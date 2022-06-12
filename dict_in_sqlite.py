import os
import sqlite3


def learning_abc():
    from abc import ABC, abstractmethod

    class Entertainer(ABC):
        @abstractmethod
        def sing(self, song):
            pass
        @abstractmethod
        def dance(self):
            pass
        def all_the_other_stuff(self, msg):
            print(msg)

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
    msg = """By subclassing Entertainer in StreetPerformer we added all the
attributes from the Entertainer to the StreetPerformer. We implemented sing and 
dance in StreetPerformer to override the ones in the base class, but we did not 
implement all_the_other_stuff in StreetPerformer and we will get it for free.
This means that subclassing can alter our class with the base class' attributes.
We did not decorate all_the_other_stuff with abstractmethod or it would raise a
TypeError at run time because all the decorated methods in the base class need 
also to be created in their subclasses."""
    StreetPerformer().all_the_other_stuff(msg=msg)


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
