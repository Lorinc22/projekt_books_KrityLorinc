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
    pass
def login():
    pass


menu()