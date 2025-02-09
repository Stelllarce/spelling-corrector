# Spelling Corrector

## Purpose

The purpose of this project is to create a simple spelling corrector that can correct spelling mistakes in a single word. This is a project that will be presented in the course "Systems Based On Knowledge" and "Programming With Python" at the University of Mathematics and Informatics in Sofia.

## Structure

The project is divided into two parts - a console application and a web application. The console application is a simple spelling corrector that can correct spelling mistakes in a single word. The web application is a more sophisticated version of the console application, which can detect languages on the run, correct spelling mistakes in a single word and auto-correct.

## Installation

To continue forward you need to have a package manager installed on your machine. If you don't have one, you can install `pip` by following the instructions [`here`](https://phoenixnap.com/kb/install-pip-windows)

To install the project you need to have `Python 3.10.15` or higher installed on your machine. You can install the project by running the following command from the root directory:

```bash
pip install -r requirements.txt
```

# Corrector Docs

## Description

### Dameau-Levenshtein distance
This spelling corrector uses the standard approach of using edit distance algoritm, namely the **Dameau-Levenshtein** distance, to correct spelling mistakes. The algorithm builds a matrix `M` of the distances between the words and then finds the shortest path between the two words, by utilising dynamic programming. The desired shortest edit-distance should be in cell `M[n -1][m -1]`.

### Selection mechanism
The selection mechanism is a simple one. The algorithm selects the word with the smallest edit distance from the misspelled word. If there are multiple words with the same edit distance, the algorithm picks the best result base on the `prob` function, that is the probability of the word appearing in the language (based on the number of times it appears in the corpus).

### Speeding up
The program uses a simple cache to store already used words an their correction. Also, when processing filess the program will deploy multiple threads to speed up the process and process multiple lines concurrently.

#### Remarks:
Candidates selection through this principle seems to be no diffrent from the simple `word_dictionary`, created by calling `Counter` on the text and sorting it from least to most edit distance.

# Using the CLA

**The program is a console application, so you will need a terminal to run it.**

## Modes

The program has two modes - `interactive` and `file`. The `interactive` mode allows the user to input a word and the program will correct it. The `file` mode allows the user to input a file and the program will correct all the words in the file.

**All modes require at least a specified maximum edit distance with the flag** `-d` **or** `--max-edit-distance`

### Interactive mode

**All commands in this mode are being processed by pressing ENTER TWICE after the command or text.**

When launched, this mode prompts the user to enter text. The program will then correct the spelling of the text and print the corrected text. Press `ENTER` twice to process.
For example:

```bash
**Start the program in interactive mode:**
python3 corrector.py -d 3

**Prompt to enter some text**
Enter text (press Enter twice to process, or '!exit' to quit):
Ths is a sentense
Waht iz ths

**Result:**
This is a sentence
What is this
```

You can exit the program by typing `!exit` and pressing `ENTER`.

### Disclaimer:
Note that the program corrects the spelling of only single words, such as:
```
Ths is a sentense -> This is a sentence
``` 
Example corrections such as the following:
```
Thisisasentence -> This is a sentence
```
are **not** yet supported.

### File mode

File mode can be launched in a single line by using flags. Like for example:

```bash
python3 corrector.py -d 3 -f file.txt
```

In this mode, the program will output the corrected copy in the same directory as the original.

#### Possible flags:
- `-d` or `--max-edit-distance` - the maximum edit distance for the algorithm to search for a correction
- `-f` or `--file` - the file to be corrected
- `-o` or `--output` - the output file [***Optional***]
- `-l` or `--language` - the language of the text (default is *'en'*) [***Optional***]
    - Possible values are *'en'* and *'bg'* currently
- `-n` or `--name` - the name of the file (default is '*corrected_<original_file_name>*') [***Optional***]

# Web Application

The web application is a more sophisticated version of the console application. It can detect languages on the run, correct spelling mistakes in a single word and auto-correct.

## Usage
**The program is a web application, so you will need a browser to run it.**

The following command runs the web app:

```bash
python3 -m web.app
```

The following command runs the uvicorn server:

```bash
python3 -m api.app
```

or 

```bash
uvicorn api.app:app --reload
```

The **website** opens on port `8000` by default and the **api** on port `5000`. The website can be accessed on all addresses like `http://127.0.0.1:8000`.

- The website has a simple interface. You can input a word in the text field and the program will correct it. The program will also detect the language of the word and correct it accordingly.

- Correction candidates are shown under the text field. The most probable is shown in the middle.

- If the user wants to correct a word automatically and replace it, he can do so by clicking the suggested word, among the 5. When this happens the correction will appear as a top suggestion next time the same word for correction is typed.

- When `Auto-correct` is enabled, the program will automatically correct the word when the user presses `SPACE`. In order for that to happen suggestions must have been loaded. (The api is not very fast, especially in bulgarian)

- The non-editable text field is just a gimmick. In reflects the text in the writing text field after the user presses `ENTER`. 

## Future work

Currently the algorithm used is a very simple one. The project will be expanded with atleast one more algorithm and some of the following features:

- Implement a more sophisticated language model (Like BK-tree or Trie or Symmetric Delete spelling correction algorithm)

- Add support for more languages

- Add support for correcting conjoined words

- Add grammar correction

- Add grammar model to improve correction accuracy

- Make output text field more useful

## Known issues

- API is very slow with bulgarian language

- Website may not work with punctuations

## Used technologies

- FastAPI and Uvicorn - API
- HTML and CSS - website front-end
- JavaScript - website event handling and handling queries to the API
- Flask - website back-end
- Python - spelling corrector

## References

- https://norvig.com/spell-correct.html
- https://people.cs.pitt.edu/~kirk/cs1501/Pruhs/Spring2006/assignments/editdistance/Levenshtein%20Distance.htm
- https://www.geeksforgeeks.org/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/
- https://web.stanford.edu/%7Ejurafsky/slp3/2.pdf
- bg data: https://chitanka.info/text/3753, https://github.com/miglen/bulgarian-wordlists/blob/master/wordlists/bg-words-validated-cyrillic.txt
- en data: https://norvig.com/big.txt
