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
    password = input("Add meg a jelszavad:")
    birth_date = input("Szuletesi datum (YYYY-MM-DD): ")
    phonenumber = input("Telefonszam: ")
def login():
    username = input("Add meg a felhasznalo neved:")
    password = input("Add meg a jelszavad:")



menu()