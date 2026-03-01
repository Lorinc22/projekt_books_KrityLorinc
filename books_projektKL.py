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
[1] Regisztrácio
[2] Bejelentkezés

""")

    if control == '1':
        register()
    elif control == '2':
        login()
    else:
        print("ilyen választas nem létezik")


def register():
    name = input("Add meg a teljes neved:")
    username = input("Add meg a felhasználo neved:")
    email = input("Add meg az emailed:")
    user_password = input("Add meg a jelszavad:")
    birth_date = input("Születési dátum (YYYY-MM-DD): ")
    phonenumber = input("Telefonszám: ")

    if len(user_password) < 8:
        print("A jelszó rövid")
        return

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Hibás Email formátum")
        return

    if not phonenumber.isdigit():
        print("Hibás Telefonszám")
        return

    if len(name.strip()) < 2:
        print("Hibás Név")
        return

    if len(username.strip()) < 3:
        print("Hibás Felhasználónév")
        return
    try:
        sql = """
                    INSERT INTO users (name, username, email, phonenumber, birth_date, user_password, user_role) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

        data = (name, username, email, phonenumber, birth_date, user_password, 'user')

        cursor.execute(sql, data)
        conn.commit()
        print("Sikeres regisztrácio!")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def login():
    username = input("Add meg a felhasználó neved:")
    password = input("Add meg a jelszavad:")
    try:
        sql = """ 
            SELECT user_password, user_role FROM users WHERE username = %s
        """
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is None:
            print("Nincs ilyen felhasználó")
        else:
            db_password = result[0]
            user_role = result[1]

            if password == db_password:
                print("Sikeres Bejelentkezés!")

                if user_role == 'admin':
                    admin_menu()
                else:
                    user_menu()
            else:
                print("Rossz jelszó")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def admin_menu():
    control = input("""
        [1] Könyvek hozzáadása
        [2] Könyvek Törlése
        [3] Könyvek Szerkesztése

        """)
    if control == '1':
        add_book()
    elif control == '2':
        remove_book()
    elif control == '3':
        change_book()
        return
    else:
        print("ilyen választás nem létezik")


def user_menu():
    control = input("""
    [1] Könyvek keresése

    """)

    if control == '1':
        usermenu2()
    else:
        print("ilyen választás nem létezik")


def usermenu2():
    control = input("""
    [1] Cím szerint keresés
    [2] Szerző szerint keresés
    [3] Kiadási dátum szerint keresés

    """)

    if control == '1':
        find_by_title()
    elif control == '2':
        find_by_author()
    elif control == '3':
        find_by_date()
    else:
        print("Ilyen választás nem létezik")


def find_by_title():
    option1 = input("Írd be a könyv címét: ")
    try:
        sql = """     
        SELECT title, author, year FROM books WHERE title ILIKE %s
        """
        cursor.execute(sql, (f"%{option1}%",))
        result = cursor.fetchall()
        if result is None:
            print("Nincs ilyen könyv")
        else:
            print("Találatok:")
            for row in result:
                print(f"- {row[0]} ({row[1]}, {row[2]})")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def find_by_author():
    option2 = input("Írd be a könyv szerzőjét: ")
    try:
        sql = """     
        SELECT title, author, year FROM books WHERE author ILIKE %s
        """
        cursor.execute(sql, (f"%{option2}%",))
        result = cursor.fetchall()
        if result is None:
            print("Nincs ilyen szerző")
        else:
            print("Találatok:")
            for row in result:
                print(f"- {row[0]} ({row[1]}, {row[2]})")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def find_by_date():
    option3 = input("Írd be a könyv kiadási dátumát: ")
    try:
        sql = """     
        SELECT title, author, year FROM books WHERE year = %s
        """
        cursor.execute(sql, (int(option3),))
        result = cursor.fetchall()
        if result is None:
            print("Nincs ilyen kiadási dátum")
        else:
            print("Találatok:")
            for row in result:
                print(f"- {row[0]} ({row[1]}, {row[2]})")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def add_book():
    title = input("Cím: ")
    author = input("Szerző: ")
    year = input("Kiadási dátum: ")

    try:
        sql = """
        INSERT INTO books (title, author, year) VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (title, author, year))
        conn.commit()
        print("Sikeres hozzáadás!")
    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def remove_book():
    title = input("Cím: ")
    author = input("Szerző: ")
    year = input("Kiadási dátum: ")
    try:
        sql = """
        DELETE FROM books WHERE title = %s AND author = %s AND year = %s
        """
        cursor.execute(sql, (title, author, int(year)))
        conn.commit()
        print("Sikeres törlés")
    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


def change_book():
    title = input("Cím: ")
    author = input("Szerző: ")
    year = input("Kiadási dátum: ")

    try:
        cursor.execute("SELECT * FROM books WHERE title = %s AND author = %s AND year = %s",
                       (title, author, int(year)))
        result = cursor.fetchone()

        if result is None:
            print("Nincs ilyen könyv az adatbázisban")
            return

        print("Talált könyv:", result)

        new_title = input("Új cím: ")
        new_author = input("Új szerző: ")
        new_year = input("Új kiadási dátum: ")

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
        print("Sikeres módosítás")

    except Exception as e:
        conn.rollback()
        print(f"Hiba történt: {e}")


menu()
cursor.close()
conn.close()
