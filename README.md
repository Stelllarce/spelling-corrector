# Python Spelling Corrector Documentation

## Purpose

The purpose of this project is to create a simple spelling corrector that can correct spelling mistakes in a text. This is a project that will be presented in the course "Systems Based On Knowledge" and "Programming With Python" at the University of Mathematics and Informatics in Sofia.

## Description

### Dameau-Levenshtein distance
This spelling corrector uses the standard approach of using edit distance algoritm, namely the Dameau-Levenshtein distance, to correct spelling mistakes. The algorithm builds a matrix **M** of the distances between the words and then finds the shortest path between the two words, by utilising dynamic programming. The desired shortest edit-distance should be in cell M[n -1][m -1].

### Selection mechanism
The selection mechanism is a simple one. The algorithm selects the word with the smallest edit distance from the misspelled word. If there are multiple words with the same edit distance, the algorithm selects the first one.

## Installation

To install the project you need to have Python 3.10.15 or higher installed on your machine. You can install the project by running the following command:

```bash
pip install -r requirements.txt
```

## Usage

To use the project you need to run the following command from the root directory of the project:

```bash
python3 src/main.py
```

## Future work

Currently the algorithm used is a very simple one. The project will be expanded with atleast one more algorithm and some of the following features:

- Implement a more sophisticated language model (Like BK-tree or Trie or Symmetric Delete spelling correction algorithm)

- Add support for more languages

- Add support for work with files

- Add support for work with text from the internet (create a simple flask app)

## References

- https://norvig.com/spell-correct.html
- https://people.cs.pitt.edu/~kirk/cs1501/Pruhs/Spring2006/assignments/editdistance/Levenshtein%20Distance.htm
- https://www.geeksforgeeks.org/introduction-to-dynamic-programming-data-structures-and-algorithm-tutorials/
- https://web.stanford.edu/%7Ejurafsky/slp3/2.pdf
- bg data: https://chitanka.info/text/3753, https://github.com/miglen/bulgarian-wordlists/blob/master/wordlists/bg-words-validated-cyrillic.txt
- en data: https://norvig.com/big.txt
- de data:  https://github.com/lorenbrichter/Words/tree/master/Words, https://archive.org/stream/in.ernet.dli.2015.168305/2015.168305.Im-Westen-Nichts-Neues_djvu.txt