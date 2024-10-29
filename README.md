# Wordle Killer

**Wordle Killer** is a powerful command-line tool designed to help you find words that fit specific criteria, making your Wordle game-solving process more efficient and enjoyable. Whether you're stuck on a tricky puzzle or looking to enhance your word game strategies, Wordle Killer provides the flexibility and precision you need.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Examples](#examples)
- [Output](#output)
- [Word List File](#word-list-file)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- **Language Support:** Currently supports Spanish and English word lists.
- **Flexible Filtering:** Filter words by length, contained letters, excluded letters, exact letter positions, and prohibited letter positions.
- **Accent Handling:** Option to include or exclude words with accented characters.
- **Output Options:** Display results in the console or save them to a file.
- **Case Insensitive:** Automatically handles uppercase and lowercase letters.

---

## Installation

### Prerequisites

- **Python 3.6 or higher** must be installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

### Clone the Repository

```bash
git clone https://github.com/tu-usuario/wordle-killer.git
cd wordle-killer
```

### Install Required Packages

Wordle Killer relies on the unidecode library for handling accented characters. Install it using pip:

```bash
pip install unidecode
```

---

## Usage

Wordle Killer is a command-line tool. You can run it using Python from your terminal or command prompt.

### Basic Syntax

```bash
python wordle_killerV4.py [OPTIONS]
```

### Command-Line Arguments

Wordle Killer offers a variety of command-line arguments to customize your search:

- **_--language, --idioma, -g_**
    - Description: Specify the language of the word list.
    - Choices: spanish, english
    - Default: spanish
    - Example: -g english

- **_--length, --longitud, -l_**
    - Description: Specify the length of the words to search for.
    - Type: Integer
    - Example: -l 5

- **_--contains, --contiene, -c_**
    - Description: Specify letters that the word must contain, separated by commas.
    - Format: a,d,e
    - Example: -c a,i,r

- **_--not-contains, --no-contiene, -nc_**
    - Description: Specify letters that the word must not contain, separated by commas.
    - Format: x,z
    - Example: -nc u,t,s,b,n,c,d,r

- **_--exact, --exacto, -e_**
    - Description: Specify exact letter positions in the format positionletter, separated by commas.
    - Format: 2f,4a,5t
    - Example: -e 4j,5a

- **_--contained-prohibited, --contiene-prohibidas, -cp_**
    - Description: Specify letters that the word must contain and cannot be in certain positions. Use the format posletter, separated by commas.
    - Format: 1a,4o,2a,5o
    - Example: -cp 1a,4o,2a,5o,2o,4a,5o

- **_--accents, --tildes, -t_**
    - Description: Filter words with or without accents.
    - Choices: true, false
    - Default: true
    - Example: -t false

- **_--out, --salida, -o_**
    - Description: Specify the output destination. Use console to print to the terminal or provide a filename to save the results.
    - Default: console
    - Example: -o resultados.txt


### Examples

#### Example 1: Basic Search

Find all 5-letter Spanish words that contain the letters a, i, r, do not contain u, t, s, b, n, c, d, r, and display the results in the console.

```bash
python wordle_killerV4.py -l 5 -c a,i,r -nc u,t,s,b,n,c,d,r
```

#### Example 2: Search with Exact and Contained-Prohibited Positions

Find all 5-letter Spanish words where:

- The letter j is in position 4.
- The letter a is in position 5.
- The word contains a and o but:
    - 'a' is not in positions 1 and 2.
    - 'o' is not in positions 4 and 5.
- The word does not contain u, t, s, b, n, c, d, r.
- Save the results to a.txt.

```bash
python wordle_killerV4.py -l 5 -e 4j,5a -cp 1a,4o,2a,5o,2o,4a,5o -nc u,t,s,b,n,c,d,r -o a.txt
```

---

## Output

Wordle Killer can display the results in two ways:

1. Console Output
    If you do not specify the --out (-o) parameter or set it to console, the results will be printed directly in your terminal or command prompt.

    ```bash
    python wordle_killerV4.py -l 5 -c a,i,r -nc u,t,s,b,n,c,d,r
    ```

    Sample Output: Found words: ['ariel', 'arisa', 'arias']

2. File Output
    Specify a filename with the --out (-o) parameter to save the results to a text file.

    ```bash
    python wordle_killerV4.py -l 5 -c a,i,r -nc u,t,s,b,n,c,d,r -o resultados.txt
    ```

    Sample Output:

    ```bash
    ariel
    arisa
    arias
    ```

---

### Word List File

Wordle Killer requires a word list file to function. By default, it looks for a file named Spanish_RAE.txt for Spanish words. If you choose English, ensure you have an appropriate English word list file.

## Preparing the Word List

1. Spanish Word List (Spanish_RAE.txt)
    - Place your Spanish word list in the same directory as the script
    - Ensure each word is on a separate line.
2. English Word List
    - Currently, English support is not implemented. If you wish to add English support in the future, ensure you have a similar word list named appropriately and update the script accordingly.

---

## Troubleshooting

If you encounter issues while using Wordle Killer, consider the following solutions:

1. Word Not Found:

    - Issue: The desired word isn't appearing in the results.
    - Solution:
        - Verify that the word exists in your word list file.
        - Check your command-line arguments for typos or incorrect formats.
2. Incorrect Exclusions/Inclusions:

    - Issue: Words that should be excluded are appearing or vice versa.
    - Solution:
        - Ensure that the -nc (not-contains) parameter is correctly specified.
        - Double-check the positions in -cp and -e to ensure they align with your requirements.

3. Script Errors:

    - Issue: Python throws errors when running the script.
    - Solution:
        - Ensure all required packages are installed (unidecode).
        - Verify that the word list file exists and is correctly named.
        - Check that the command-line arguments follow the correct format.
4. Accents Handling:

    - Issue: Words with accents are incorrectly included or excluded.
    - Solution:
        - Use the --accents (-t) parameter to control whether to include (true) or exclude (false) accented words.
        - Ensure that your word list accurately represents accented characters.

---

## License

This project is licensed under the MIT License.

---

### Happy Word Hunting!

If you have any questions or need further assistance, feel free to reach out or open an issue in the repository.
