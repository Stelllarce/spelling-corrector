# Python Spelling Corrector Documentation

## Purpose

The purpose of this project is to create a simple spelling corrector that can correct spelling mistakes in a text. This is a project that will be presented in the course "Systems Based On Knowledge" and "Programming With Python" at the University of Mathematics and Informatics in Sofia.

## Description

This spelling corrector uses the standard approach of using edit distance algoritm, namely the Dameau-Levenshtein distance, to correct spelling mistakes. It also uses a language model to correct the mistakes. The language model is based on the probability of a word given the previous word. The language model is trained on a large corpus of text.

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