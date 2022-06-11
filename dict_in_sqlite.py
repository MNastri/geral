import os
import sqlite3


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
    main()
