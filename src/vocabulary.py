import os
import uuid


dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, 'data/Swadesh200.csv'), 'r', encoding='utf-8') as file:
    raw_data = [i.replace('\n', '').split(',') for i in file.readlines()[1:]]
    SWADESH = [(i[0], int(i[1]), int(i[2])) for i in raw_data]


class Vocabulary:
    def __init__(self, id: str = ''):
        self.items = []
        self.id = id if id else str(uuid.uuid4())

    def add_item(self, definition, word):
        self.items.append({
            "definition": definition,
            "word": word
        })

    def has_word(self, word):
        return any([item['word'] == word for item in self.items])

    def get_word(self, word):
        return next((item for item in self.items if item['word'] == word), None)

    def get_definition(self, definition):
        return next((item for item in self.items if item['definition'] == definition), None)

    def __str__(self):
        return '\n'.join([f"{item['word']} : {item['definition']}" for item in self.items])

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __iter__(self):
        return iter(self.items)

    def to_json(self) -> dict:
        return {
            "items": self.items,
            "id": self.id
        }

    @staticmethod
    def from_json(data: dict) -> 'Vocabulary':
        vocabulary = Vocabulary(data['id'])
        vocabulary.items = data['items']
        return vocabulary

    @staticmethod
    def from_csv(file_path: str) -> 'Vocabulary':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = [i.replace('\n', '').split(',') for i in file.readlines()]
            vocabulary = Vocabulary()
            for item in data:
                vocabulary.add_item(item[0], item[1])
        return vocabulary
