def save_to_txt(results):
    with open('book.txt', 'w', encoding="utf-8") as file:
        for row in results:
            file.write(f"{row[0]} ({row[1]}, {row[2]})\n")
    print("Eredmény sikeresen elmentve a book.txt fájlba")
