import argparse
import unidecode
from collections import defaultdict

def load_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip().lower() for line in file]
    return words

def get_variants(letter):
    """
    Devuelve una lista de variantes de la letra proporcionada,
    incluyendo la versión con acento si es aplicable.
    """
    accented_letters = {
        'a': ['a', 'á'],
        'e': ['e', 'é'],
        'i': ['i', 'í'],
        'o': ['o', 'ó'],
        'u': ['u', 'ú'],
    }
    return accented_letters.get(letter.lower(), [letter.lower()])

def has_accents(word, allowed_letters):
    """
    Verifica si la palabra contiene acentos en letras que no están permitidas.
    Las letras permitidas son aquellas especificadas en allowed_letters.
    """
    for letter in word:
        base = unidecode.unidecode(letter.lower())
        if letter.lower() == base:
            continue  # Sin acento
        # Si la letra base está en allowed_letters, permitimos su variante acentuada
        if base in allowed_letters:
            continue
        return True  # Tiene acento en una letra no permitida
    return False

def search_words(words, length=None, contain_letters_counts=None, exact_letters_positions=None, exact_letters_counts=None, include_accents=True, excluded_letters=None, prohibited_letters_positions=None):
    results = words

    # Filtrar por longitud
    if length:
        results = [word for word in results if len(word) == length]

    # Filtrar por posiciones exactas
    if exact_letters_positions:
        for position, letter in exact_letters_positions:
            variants = get_variants(letter)
            results = [word for word in results if len(word) > position and word[position] in variants]

    # Filtrar por letras contenidas con cuentas
    if contain_letters_counts:
        for letter, count in contain_letters_counts.items():
            variants = get_variants(letter)
            required = count + exact_letters_counts.get(letter, 0)
            # Mover la suma dentro de la comprensión de lista
            results = [word for word in results if sum(word.count(v) for v in variants) >= required]

    # Filtrar por acentos si no se permiten
    if not include_accents:
        allowed_letters = set()
        # Añadir letras de -c y -e a las permitidas para acentos
        if contain_letters_counts:
            allowed_letters.update(contain_letters_counts.keys())
        if exact_letters_positions:
            for _, letter in exact_letters_positions:
                allowed_letters.add(letter.lower())
        results = [word for word in results if not has_accents(word, allowed_letters)]

    # Filtrar por letras excluidas
    if excluded_letters:
        for letter in excluded_letters:
            variants = get_variants(letter)
            if contain_letters_counts and letter in contain_letters_counts:
                allowed_count = contain_letters_counts[letter] + exact_letters_counts.get(letter, 0)
            elif exact_letters_counts and letter in exact_letters_counts:
                allowed_count = exact_letters_counts.get(letter, 0)
            else:
                allowed_count = 0
            # Filtrar palabras que tengan <= allowed_count de la letra, considerando variantes
            results = [word for word in results if sum(word.count(v) for v in variants) <= allowed_count]

    # Filtrar por posiciones prohibidas de letras contenidas
    if prohibited_letters_positions:
        for letter, positions in prohibited_letters_positions.items():
            variants = get_variants(letter)
            # Excluir palabras que tengan alguna de las variantes de la letra en las posiciones prohibidas
            results = [word for word in results if all(word[pos] not in variants for pos in positions if pos < len(word))]

    return results

def parse_query(args):
    length = args.length

    # Procesar letras contenidas (-c) y contar duplicados
    contained_letters = args.contains.split(",") if args.contains else []
    contained_letters_counts = defaultdict(int)
    for letter in contained_letters:
        if letter:  # Evitar letras vacías
            contained_letters_counts[letter.lower()] += 1

    # Procesar letras excluidas (-nc)
    excluded_letters = args.not_contains.split(",") if args.not_contains else []
    excluded_letters = [letter.lower() for letter in excluded_letters if letter]  # Eliminar posibles letras vacías

    # Procesar posiciones exactas (-e)
    exact_letters_positions = []
    if args.exact:
        exact_pairs = args.exact.split(",")
        for pair in exact_pairs:
            if len(pair) < 2:
                continue  # Ignorar pares inválidos
            position_part = pair[:-1]
            letter = pair[-1].lower()
            if position_part.isdigit():
                position = int(position_part) - 1  # Ajuste para índice basado en 0
                exact_letters_positions.append((position, letter))

    # Contar ocurrencias de letras en posiciones exactas
    exact_letters_counts = defaultdict(int)
    for _, letter in exact_letters_positions:
        exact_letters_counts[letter] += 1

    # Procesar letras contenidas con posiciones prohibidas (-cp)
    prohibited_letters_positions = defaultdict(set)
    if args.contained_prohibited:
        cp_pairs = args.contained_prohibited.split(",")
        for pair in cp_pairs:
            if len(pair) < 2:
                continue  # Ignorar pares inválidos
            position_part = pair[:-1]
            letter = pair[-1].lower()
            if position_part.isdigit():
                position = int(position_part) - 1  # Ajuste para índice basado en 0
                prohibited_letters_positions[letter].add(position)
    # Añadir cada letra única en -cp a contain_letters_counts solo una vez, si no está en exact_letters_counts
    for letter in prohibited_letters_positions:
        if letter not in exact_letters_counts:
            contained_letters_counts[letter] = max(contained_letters_counts[letter], 1)

    return length, contained_letters_counts, exact_letters_positions, excluded_letters, exact_letters_counts, prohibited_letters_positions

def main():
    parser = argparse.ArgumentParser(description="Search words in a text file based on specific criteria")
    parser.add_argument("--language", "--idioma", "-g", choices=["spanish", "english"], default="spanish", help="Language of the word list (default is Spanish)")
    parser.add_argument("--length", "--longitud", "-l", type=int, help="Length of the words")
    parser.add_argument("--contains", "--contiene", "-c", help="Letters the word should contain, separated by commas (e.g., a,d,e)")
    parser.add_argument("--not-contains", "--no-contiene", "-nc", help="Letters the word should NOT contain, separated by commas (e.g., x,z)")
    parser.add_argument("--exact", "--exacto", "-e", help="Positions and letters in the format 'positionletter', separated by commas (e.g., 2f,4a,5t)")
    parser.add_argument("--contained-prohibited", "--contiene-prohibidas", "-cp", help="Letters the word should contain with prohibited positions, in the format 'posletter', separated by commas (e.g., 2a,3a,5b,2c)")
    parser.add_argument("--accents", "--tildes", "-t", type=str, choices=["true", "false"], default="true", help="Filter words with (true) or without (false) accents")
    parser.add_argument("--out", "--salida", "-o", nargs="?", const="console", help="Output destination: 'console' (default) or specify a file name")

    args = parser.parse_args()

    if args.language == "spanish":
        words = load_words("Spanish_RAE.txt")
    elif args.language == "english":
        print("NOT IMPLEMENTED YET")
        exit()

    # Procesar parámetros de búsqueda
    (length, 
     contain_letters_counts, 
     exact_letters_positions, 
     excluded_letters, 
     exact_letters_counts, 
     prohibited_letters_positions) = parse_query(args)
    
    include_accents = args.accents.lower() == "true"

    # Realizar la búsqueda
    results = search_words(
        words,
        length=length,
        contain_letters_counts=contain_letters_counts,
        exact_letters_positions=exact_letters_positions,
        exact_letters_counts=exact_letters_counts,
        include_accents=include_accents,
        excluded_letters=excluded_letters,
        prohibited_letters_positions=prohibited_letters_positions
    )

    # Salida de resultados
    if not args.out or args.out == "console":
        print("Found words:", results)
    else:
        with open(args.out, 'w', encoding='utf-8') as output_file:
            for word in results:
                output_file.write(f"{word}\n")
        print(f"Results saved to {args.out}")

if __name__ == "__main__":
    main()
