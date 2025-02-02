"""
Vocabulary Module

This module provides functionality to manage a collection of words and their glosses.
The main class, `Vocabulary`, allows for adding, retrieving, and exporting word-gloss pairs.
It supports loading and saving vocabularies from/to CSV, text, and JSON files.
"""

import csv
import json
from pathlib import Path
from typing import Any, List, Dict, Iterator
from .word import Word


class Vocabulary:
    """
    A class to manage a collection of words and their glosses.

    Attributes:
        items (List[Dict[str, Any]]): A list of dictionaries with 'word' and 'gloss' keys.
                                      Where 'word' is a Word object and 'gloss' is a string.
    """

    def __init__(self):
        """
        Initialize an empty vocabulary.
        """
        self.items: List[Dict[str, Any]] = []

    def add_item(self, word: Word, gloss: str) -> None:
        """
        Add a word and its gloss to the vocabulary.

        Args:
            word (Word): The word to add.
            gloss (str): The gloss or meaning of the word.
        """
        self.items.append({'word': word, 'gloss': gloss})

    def has_word(self, word: Word) -> bool:
        """
        Check if the vocabulary contains a specific word.

        Args:
            word (Word): The word to check.

        Returns:
            bool: True if the word exists, False otherwise.
        """
        return any(item['word'] == word for item in self.items)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """
        Iterate over the vocabulary items.

        Yields:
            Iterator[Dict[str, Any]]: A dictionary containing 'word' and 'gloss'.
        """
        for item in self.items:
            yield (item['word'], item['gloss'])

    def __str__(self) -> str:
        """
        Convert the vocabulary to a string representation.

        Returns:
            str: A string with each word-gloss pair on a new line in "word: gloss" format.
        """
        return "\n".join(f"{item['word']}: {item['gloss']}" for item in self.items)

    def __repr__(self) -> str:
        """
        Return the string representation of the vocabulary for debugging.

        Returns:
            str: A string representation of the vocabulary.
        """
        return f"Vocabulary({self.items})"

    def __getitem__(self, key) -> str:
        """
        Get a word-gloss pair from the vocabulary.

        Args:
            key (int or slice): The index or slice to retrieve.
        
        Returns:
            str: The word-gloss pair at the specified index or indices.
        """
        if isinstance(key, int):
            return f"{self.items[key]['word']}: {self.items[key]['gloss']}"
        if isinstance(key, slice):
            return "\n".join(f"{item['word']}: {item['gloss']}" for item in self.items[key])

    def __len__(self) -> int:
        """
        Get the number of word-gloss pairs in the vocabulary.
        """
        return len(self.items)

    def to_csv(self, filename: str) -> None:
        """
        Save the vocabulary to a CSV file.

        Args:
            filename (str): Path to the output CSV file.
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['word', 'gloss'])
            writer.writeheader()
            writer.writerows(self.items)

    def to_txt(self, filename: str) -> None:
        """
        Save the vocabulary to a text file.

        Args:
            filename (str): Path to the output text file.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(self))

    @staticmethod
    def _parse_lines(lines: List[str], delimiter: str = ': ') -> List[Dict[str, Any]]:
        """
        Parse lines of text to extract word-gloss pairs.

        Args:
            lines (List[str]): The lines to parse.
            delimiter (str): The delimiter separating words and glosses.

        Returns:
            List[Dict[str, Any]]: A list of parsed word-gloss dictionaries.
        """
        items = []
        for line in lines:
            if delimiter in line:
                word, gloss = line.strip().split(delimiter, 1)
                items.append({'word': Word(word), 'gloss': gloss})
        return items

    @staticmethod
    def from_str(string: str) -> 'Vocabulary':
        """
        Create a Vocabulary object from a string.

        Args:
            string (str): The input string with word-gloss pairs.

        Returns:
            Vocabulary: A new Vocabulary object.
        """
        vocabulary = Vocabulary()
        lines = string.strip().split('\n')
        vocabulary.items = Vocabulary._parse_lines(lines)
        return vocabulary

    @staticmethod
    def from_csv(filename: str) -> 'Vocabulary':
        """
        Create a Vocabulary object from a CSV file.

        Args:
            filename (str): Path to the input CSV file.

        Returns:
            Vocabulary: A new Vocabulary object.
        """
        vocabulary = Vocabulary()
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'word' in row and 'gloss' in row:
                    vocabulary.add_item(Word(row['word']), row['gloss'])
        return vocabulary

    @staticmethod
    def from_txt(file_path: str) -> 'Vocabulary':
        """
        Create a Vocabulary object from a text file.

        Args:
            file_path (str): Path to the input text file.

        Returns:
            Vocabulary: A new Vocabulary object.
        """
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f'File not found: {file_path}')
        with path.open('r', encoding='utf-8') as f:
            return Vocabulary.from_str(f.read())

    @staticmethod
    def from_list(items: List[Dict[str, Any]]) -> 'Vocabulary':
        """
        Create a Vocabulary object from a list of word-gloss dictionaries.

        Args:
            items (List[Dict[str, str]]): A list of word-gloss dictionaries.

        Returns:
            Vocabulary: A new Vocabulary object.
        """
        vocabulary = Vocabulary()
        vocabulary.items = items
        return vocabulary

    @staticmethod
    def from_json(file_path: str) -> 'Vocabulary':
        """
        Create a Vocabulary object from a JSON file.

        Args:
            file_path (str): Path to the input JSON file.

        Returns:
            Vocabulary: A new Vocabulary object.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        return Vocabulary.from_list(items)
