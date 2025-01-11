class Vocabulary:
    def __init__(self):
        self.items = []

    def add_item(self, word: str, gloss: str) -> None:
        self.items.append({'word': word, 'gloss': gloss})

    def has_word(self, word: str) -> bool:
        return any(item['word'] == word for item in self.items)

    def __iter__(self):
        for item in self.items:
            yield (item['word'], item['gloss'])

    def to_csv(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write('word,gloss\n')
            for item in self.items:
                f.write(f"{item['word']},{item['gloss']}\n")
    
    def to_str(self) -> str:
        return '\n'.join(f"{item['word']}: {item['gloss']}" for item in self.items)

    def to_txt(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(self.to_str())

    @staticmethod
    def from_str(string: str) -> 'Vocabulary':
        vocabulary = Vocabulary()
        for line in string.split('\n'):
            try:
                word, gloss = line.strip().split(': ')
                vocabulary.add_item(word, gloss)
            except ValueError:
                continue
        return vocabulary

    @staticmethod
    def from_csv(filename: str) -> 'Vocabulary':
        vocabulary = Vocabulary()
        with open(filename, 'r') as f:
            next(f)
            for line in f:
                try:
                    word, gloss = line.strip().split(',')
                    vocabulary.add_item(word, gloss)
                except ValueError:
                    continue
        return vocabulary

    @staticmethod
    def from_txt(filename: str) -> 'Vocabulary':
        with open(filename, 'r') as f:
            return Vocabulary.from_str(f.read())
