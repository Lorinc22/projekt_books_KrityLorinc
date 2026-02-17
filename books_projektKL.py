import cursor
import psycopg2

config ={
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



menu()
cursor.close()
conn.close()