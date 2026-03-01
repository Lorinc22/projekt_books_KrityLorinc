import re

import cursor
import psycopg2

config = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
}
try:
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    print("connected")
except psycopg2.DatabaseError as error:
    print(error)
    exit()


def menu():
    control = input("""
[1] Regisztracio
[2] bejelentkezes

""")

    if control == '1':
        register()
    elif control == '2':
        login()
    else:
        print("ilyen valasztas nem letezik")


def register():
    name = input("Add meg a teljes neved:")
    username = input("Add meg a felhasznalo neved:")
    email = input("Add meg az emailed:")
    user_password = input("Add meg a jelszavad:")
    birth_date = input("Szuletesi datum (YYYY-MM-DD): ")
    phonenumber = input("Telefonszam: ")

    if len(user_password) < 8:
        print("A jelszo tul rovid")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Hibas Email formatum")
        return

    if not phonenumber.isdigit():
        print("Hibas Telefonszam")
        return

    if len(name.strip()) < 2:
        print("Hibas Nev")
        return

    if len(username.strip()) < 3:
        print("Hibas Felhasznalonev")
        return
    try:
        sql = """
                    INSERT INTO users (name, username, email, phonenumber, birth_date, user_password, user_role) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

        data = (name, username, email, phonenumber, birth_date, user_password, 'user')

        cursor.execute(sql, data)
        conn.commit()
        print("Sikeres regisztracio!")

    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def login():
    username = input("Add meg a felhasznalo neved:")
    password = input("Add meg a jelszavad:")
    try:
        sql = """ 
            SELECT user_password, user_role FROM users WHERE username = %s
        """
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is None:
            print("Nincs ilyen felhasznalo")
        else:
            db_password = result[0]
            user_role = result[1]

            if password == db_password:
                print("Sikeres Bejelentkezes!")

                if user_role == 'admin':
                    admin_menu()
                else:
                    user_menu()
            else:
                print("Rossz jelszo")

    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def admin_menu():
    control = input("""
        [1] Konyvek hozzadasa
        [2] Konyvek Torlese
        [3] Konyvek Szerkesztese

        """)
    if control == '1':
        add_book()
    elif control == '2':
        remove_book()
    elif control == '3':
        change_book()
        return
    else:
        print("ilyen valasztas nem letezik")


def user_menu():
    control = input("""
    [1] Konyvek keresese

    """)

    if control == '1':
        usermenu2()
    else:
        print("ilyen valasztas nem letezik")


def usermenu2():
    control = input("""
    [1] Cim Szerint kereses
    [2] Szero Szerint kereses
    [3] KiadasiDatum Szerint kereses

    """)

    if control == '1':
        find_by_title()
    elif control == '2':
        find_by_author()
    elif control == '3':
        find_by_date()
    else:
        print("ilyen valasztas nem letezik")


def find_by_title():
    option1 = input("Ird be a konyv cimet:")
    try:
        sql = """     
        SELECT title, author, year FROM books WHERE title ILIKE %s
        """
        cursor.execute(sql, (f"%{option1}%",))
        result = cursor.fetchall()
        if result is None:
            print("Nincs ilyen konyv")
        else:
            print("Találatok:")
            for row in result:
                print(f"- {row[0]} ({row[1]}, {row[2]})")

    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def find_by_author():
    option2 = input("Ird be a konyv szerzojet:")
    try:
        sql = """     
        SELECT title, author, year FROM books WHERE author ILIKE %s
        """
        cursor.execute(sql, (f"%{option2}%",))
        result = cursor.fetchall()
        if result is None:
            print("Nincs ilyen szerzo")
        else:
            print("Találatok:")
            for row in result:
                print(f"- {row[0]} ({row[1]}, {row[2]})")

    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def find_by_date():
    option3 = input("Ird be a konyv kiadasi datumat:")
    try:
        sql = """     
        SELECT title, author, year FROM books WHERE year = %s
        """
        cursor.execute(sql, (int(option3),))
        result = cursor.fetchall()
        if result is None:
            print("Nincs ilyen kiadasi datum")
        else:
            print("Találatok:")
            for row in result:
                print(f"- {row[0]} ({row[1]}, {row[2]})")

    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def add_book():
    title = input("Cim: ")
    author = input("Szerzo: ")
    year = input("KiadasiDatum: ")

    try:
        sql = """
        INSERT INTO books (title, author, year) VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (title, author, year))
        conn.commit()
        print("Sikeres Hozzadasa!")
    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def remove_book():
    title = input("Cim: ")
    author = input("Szerzo: ")
    year = input("KiadasiDatum: ")
    try:
        sql = """
        DELETE FROM books WHERE title = %s AND author = %s AND year = %s
        """
        cursor.execute(sql, (title, author, int(year)))
        conn.commit()
        print("Sikeres Torles")
    except Exception as e:
        conn.rollback()
        print(f"Hiba tortent: {e}")


def change_book():
    title = input("Cim: ")
    author = input("Szerzo: ")
    year = input("KiadasiDatum: ")

    try:
        cursor.execute("SELECT * FROM books WHERE title = %s AND author = %s AND year = %s",
                       (title, author, int(year)))
        result = cursor.fetchone()

        if result is None:
            print("Nincs ilyen Konyv az adatbazisban")
            return

        print("Talalt Konyv:", result)

        new_title = input("Cim: ")
        new_author = input("Szerzo: ")
        new_year = input("KiadasiDatum: ")

        if not new_title:
            new_title = title
        if not new_author:
            new_author = author
        if not new_year:
            new_year = year

        cursor.execute("""
        UPDATE books SET title = %s, author = %s, year = %s WHERE title = %s AND author = %s AND year = %s
        """, (new_title, new_author, int(new_year), title, author, int(year)))
        conn.commit()
        print("Sikeres Modositas")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


menu()
cursor.close()
conn.close()
