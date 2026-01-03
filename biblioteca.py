import csv

from anyio.streams import file

from libro import Libro

def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open (file_path, 'r', encoding='utf-8') as f:
            reader=csv.reader(f)
            for riga in reader:
                if len(riga) == 1:
                    num_sezioni = int(riga[0]) #prima riga = numero sezioni
                    biblioteca= crea_biblioteca(num_sezioni)

                if len(riga) == 5:
                    titolo, autore, anno, pagine, sezione = riga
                    libro= Libro(titolo.strip(), autore.strip(), int(anno), int(pagine))
                    biblioteca[int(sezione)-1].append(libro)

        print(f"File ''{file_path}'' caricato correttamente con {num_sezioni} sezioni")
        return biblioteca

    except FileNotFoundError:
        print(f"Errore: il file '{file_path}' non esiste.")
        return None


def crea_biblioteca(num_sezioni): #metodo interno per inizializzare la biblioteca
    return [[] for i in range(num_sezioni)]


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""

    if sezione < 1 or sezione > len(biblioteca): #se la sezione non è nella biblioteca
        return None

    if cerca_libro(biblioteca, titolo) is not None: #se il libro già c'è non lo aggiungere
        return None

    libro= Libro(titolo, autore, anno, pagine)
    biblioteca[sezione-1].append(libro)

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([libro.titolo, libro.autore, libro.anno, libro.pagine, sezione])

        print(f'File aggiornato con i nuovi libri')

    except FileNotFoundError:
        #se il file non viene trovato non è possibile aggiungere il libro, lo elimino dalla lista
        biblioteca[sezione-1].remove(libro)
        print(f'''Errore: impossibile aggiornare il file '{file_path}' perché non esiste''')
        return None

    return libro


def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""

    for numero_sezione, sezione in enumerate(biblioteca, start=1): #numero_sezioni deve partire da 1 e non da 0
        for libro in sezione:
            if libro.titolo == titolo:
                return f"{libro.titolo}, {libro.autore}, {libro.anno}, {libro.pagine}, {numero_sezione}"
    return None


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    # TODO
    if sezione < 1 or sezione > len(biblioteca) :
        print("Sezione non valida")
        return None

    titoli = [libro.titolo for libro in biblioteca[sezione-1]]
    return sorted(titoli)


def main():
    biblioteca = {}
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

