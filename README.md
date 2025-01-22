# Python Spelling Corrector Documentation

## Purpose

The purpose of this project is to create a simple spelling corrector that can correct spelling mistakes in a single word. This is a project that will be presented in the course "Systems Based On Knowledge" and "Programming With Python" at the University of Mathematics and Informatics in Sofia.

## Description

### Dameau-Levenshtein distance
This spelling corrector uses the standard approach of using edit distance algoritm, namely the Dameau-Levenshtein distance, to correct spelling mistakes. The algorithm builds a matrix **M** of the distances between the words and then finds the shortest path between the two words, by utilising dynamic programming. The desired shortest edit-distance should be in cell M[n -1][m -1].

### Selection mechanism
The selection mechanism is a simple one. The algorithm selects the word with the smallest edit distance from the misspelled word. If there are multiple words with the same edit distance, the algorithm selects the first one.

## Installation

To continue forward you need to have a package manager installed on your machine. If you don't have one, you can install `pip` by following the instructions [`here`](https://phoenixnap.com/kb/install-pip-windows)

To install the project you need to have `Python 3.10.15` or higher installed on your machine. You can install the project by running the following command from the root directory:

```bash
pip install -r requirements.txt
```

## Usage
**The program is a console application, so you will need a terminal to run it.**

To use the project you need to run the following command from the root directory of the project:

```bash
python3 src/main.py
```

or

```bash
python src/main.py
```

### Commands

You will initially be prompted to enter the **max edit-distance** you want to search for. Then you may choose **en** for inputting english or **bg** for bulgarian. After that you will be prompted to enter some text. You may enter text to be corrected or input one of these commands:

- `!exit` - to exit the program
- `!change` - to change the language
- `!file <path>` - to read text from a file

Whatever your input is, ***it will be processed after inputting two consecutive new lines after it***.

<br> When entering a file to correct, the corrected file will be saved in the same directory as the original file with the name `corrected_<original_file_name>`

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

## Future work

Currently the algorithm used is a very simple one. The project will be expanded with atleast one more algorithm and some of the following features:

- Implement a more sophisticated language model (Like BK-tree or Trie or Symmetric Delete spelling correction algorithm)

- Add support for more languages

- Add support for work with text from the internet (create a simple flask app)

- Add support for correcting conjoined words

## References

- https://norvig.com/spell-correct.html
- https://people.cs.pitt.edu/~kirk/cs1501/Pruhs/Spring2006/assignments/editdistance/Levenshtein%20Distance.htm
- https://www.geeksforgeeks.org/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/
- https://web.stanford.edu/%7Ejurafsky/slp3/2.pdf
- bg data: https://chitanka.info/text/3753, https://github.com/miglen/bulgarian-wordlists/blob/master/wordlists/bg-words-validated-cyrillic.txt
- en data: https://norvig.com/big.txt
- de data:  https://github.com/lorenbrichter/Words/tree/master/Words, https://archive.org/stream/in.ernet.dli.2015.168305/2015.168305.Im-Westen-Nichts-Neues_djvu.txt