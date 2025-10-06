import csv

def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open ('file_path', 'r', encoding='utf-8') as f:
            reader=csv.reader(f)
            righe=[riga for riga in reader]

            numSezioni=int(righe[0][0].strip())

            biblioteca={}

            for riga in righe:
                titolo = riga[0].strip()
                autore = riga[1].strip()
                anno = int(riga[2].strip())
                pagine = int(riga[3].strip())
                sezione = int(riga[4].strip())

            if sezione in biblioteca:
                libro={
                    "titolo": titolo,
                    "autore": autore,
                    "anno": anno,
                    "pagine": pagine,
                    "sezione": sezione
                }

            biblioteca[sezione].append(libro)

        return biblioteca

    except FileNotFoundError:
        print(f"File '{file_path}' non trovato.")
        return None


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""

    if sezione not in biblioteca:
        return None

    titolo_norm = titolo.strip().lower()
    for sezione in biblioteca:
        for libro in sezione:
            if libro[0].strip().lower() == titolo_norm:
                return None #perché il titolo è già presente
    libro = {
        "titolo": titolo,
        "autore": autore,
        "anno": anno,
        "pagine": pagine,
        "sezione": sezione
    }

    biblioteca[sezione].append(libro)


    with open(file_path, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([titolo, autore, anno, pagine, sezione])
    return libro



def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""

    titolo_norm = titolo.strip().lower()
    for sezione in biblioteca:
        for libro in sezione:
            if libro["titolo"].strip().lower() == titolo_norm:
                return f"{libro['titolo']}, {libro['autore']}, {libro['anno']}, {libro['pagine']}, {libro['sezione']}"
            else:
                return None




def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    # TODO
    if sezione not in biblioteca:
        return None

    titoli = [libro["titolo"] for libro in biblioteca[sezione]]
    return sorted(titoli, key=str.lower)


def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

