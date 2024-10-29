import argparse
import unidecode

def load_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]
    return words

def search_words(words, length=None, contained_letters=None, exact_letters_positions=None, include_accents=True, excluded_letters=None):
    results = words
    if length:
        results = [word for word in results if len(word) == length]
    if contained_letters:
        results = [word for word in results if all(letter in word for letter in contained_letters)]
    if exact_letters_positions:
        for position, letter in exact_letters_positions:
            results = [word for word in results if len(word) > position and word[position] == letter]
    if not include_accents:
        results = [word for word in results if word == unidecode.unidecode(word)]
    if excluded_letters:
        results = [word for word in results if all(letter not in word for letter in excluded_letters)]
    return results

def parse_query(args):
    length = args.length
    contained_letters = args.contains.split(",") if args.contains else []
    excluded_letters = args.not_contains.split(",") if args.not_contains else []
    exact_letters_positions = []

    if args.exact:
        exact_pairs = args.exact.split(",")
        for pair in exact_pairs:
            position = int(pair[:-1]) - 1  # Ajuste para índice basado en 0
            letter = pair[-1]
            exact_letters_positions.append((position, letter))

    return length, contained_letters, exact_letters_positions, excluded_letters

def main():
    parser = argparse.ArgumentParser(description="Search words in a text file based on specific criteria")
    parser.add_argument("--language", "--idioma", "-g", choices=["spanish", "english"], default="spanish", help="Language of the word list (default is Spanish)")
    parser.add_argument("--length", "--longitud", "-l", type=int, help="Length of the words")
    parser.add_argument("--contains", "--contiene", "-c", help="Letters the word should contain, separated by commas (e.g., a,d,e)")
    parser.add_argument("--not-contains", "--no-contiene", "-nc", help="Letters the word should NOT contain, separated by commas (e.g., x,z)")
    parser.add_argument("--exact", "--exacto", "-e", help="Positions and letters in the format 'positionletter', separated by commas (e.g., 2f,4a,5t)")
    parser.add_argument("--accents", "--tildes", "-t", type=str, choices=["true", "false"], default="true", help="Filter words with (true) or without (false) accents")
    parser.add_argument("--out", "--salida", "-o", nargs="?", const="console", help="Output destination: 'console' (default) or specify a file name")

    args = parser.parse_args()

    if args.language == "spanish":
        words = load_words("Spanish_RAE.txt")
    elif args.language == "english":
        print("NOT IMPLEMENTED YET")
        exit()

    # Process search parameters
    length, contained_letters, exact_letters_positions, excluded_letters = parse_query(args)
    include_accents = args.accents.lower() == "true"
    
    # Perform the search
    results = search_words(
        words,
        length=length,
        contained_letters=contained_letters,
        exact_letters_positions=exact_letters_positions,
        include_accents=include_accents,
        excluded_letters=excluded_letters
    )

    # Output results
    if not args.out:
        print("Found words:", results)
    else:
        with open(args.out, 'w', encoding='utf-8') as output_file:
            for word in results:
                output_file.write(f"{word}\n")
        print(f"Results saved to {args.out}")

if __name__ == "__main__":
    main()
