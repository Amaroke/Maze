import sqlite3


def connexion_curseur() -> tuple:
    conn = sqlite3.connect("performances.db")
    # https://docs.python.org/3/library/sqlite3.html#sqlite3-transaction-control-isolation-level
    conn.isolation_level = None
    cur = conn.cursor()
    return conn, cur


def fermer_connexion(conn: sqlite3.Connection, cur: sqlite3.Cursor):
    cur.close()
    conn.close()


def modifier(requete: str, parametres=None) -> None:
    conn, cur = connexion_curseur()
    if parametres is None:
        cur.execute(requete)
    else:
        cur.execute(requete, parametres)
    conn.commit()
    fermer_connexion(conn, cur)


def lire(requete: str, parametres=None, multiples=False) -> None:
    conn, cur = connexion_curseur()
    if parametres is None:
        cur.execute(requete)
    else:
        cur.execute(requete, parametres)
    if multiples:
        resultat = cur.fetchall()
    else:
        resultat = cur.fetchone()
    fermer_connexion(conn, cur)
    return resultat
