import csv

from pathlib import Path
from typing import List, Dict, Iterator


class Vocabulary:
    """
    A class to manage a collection of words and their glosses.

    Attributes:
        items (List[Dict[str, str]]): A list of dictionaries with 'word' and 'gloss' keys.
    """
    def __init__(self):
        """Initialize an empty vocabulary."""
        self.items: List[Dict[str, str]] = []

    def add_item(self, word: str, gloss: str) -> None:
        """
        Add a word and its gloss to the vocabulary.

        Args:
            word (str): The word to add.
            gloss (str): The gloss or meaning of the word.
        """
        self.items.append({'word': word, 'gloss': gloss})

    def has_word(self, word: str) -> bool:
        """
        Check if the vocabulary contains a specific word.

        Args:
            word (str): The word to check.

        Returns:
            bool: True if the word exists, False otherwise.
        """
        return any(item['word'] == word for item in self.items)

    def __iter__(self) -> Iterator[Dict[str, str]]:
        """
        Iterate over the vocabulary items.

        Yields:
            Iterator[Dict[str, str]]: A dictionary containing 'word' and 'gloss'.
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
        Return the string representation of the vocabulary.

        Returns:
            str: A string representation of the vocabulary.
        """
        return self.__str__()

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

    def to_str(self) -> str:
        """
        Convert the vocabulary to a string representation.

        Returns:
            str: A string with each word-gloss pair on a new line in "word: gloss" format.
        """
        return '\n'.join(f"{item['word']}: {item['gloss']}" for item in self.items)

    def to_txt(self, filename: str) -> None:
        """
        Save the vocabulary to a text file.

        Args:
            filename (str): Path to the output text file.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_str())

    @staticmethod
    def _parse_lines(lines: List[str], delimiter: str = ': ') -> List[Dict[str, str]]:
        """
        Parse lines of text to extract word-gloss pairs.

        Args:
            lines (List[str]): The lines to parse.
            delimiter (str): The delimiter separating words and glosses.

        Returns:
            List[Dict[str, str]]: A list of parsed word-gloss dictionaries.
        """
        items = []
        for line in lines:
            if delimiter in line:
                word, gloss = line.strip().split(delimiter, 1)
                items.append({'word': word, 'gloss': gloss})
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
                    vocabulary.add_item(row['word'], row['gloss'])
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
    def from_list(items: List[Dict[str, str]]) -> 'Vocabulary':
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
        import json

        with open(file_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        return Vocabulary.from_list(items)
