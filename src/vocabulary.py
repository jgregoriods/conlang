import os


dirname = os.path.dirname(__file__)

with open(os.path.join(dirname, 'data/Swadesh200.csv'), 'r', encoding='utf-8') as file:
    raw_data = [i.replace('\n', '').split(',') for i in file.readlines()[1:]]
    SWADESH = [(i[0], int(i[1]), int(i[2])) for i in raw_data]


class Vocabulary:
    def __init__(self, language):
        self.language = language
        self.items = []

    def add_item(self, definition, word):
        self.items.append({
            "definition": definition,
            "word": word
        })

    def has_word(self, word):
        return word in [w['word'] for w in self.items]

    def __str__(self):
        res = ""
        for i in self.items:
            res += f"{i['definition']}: {i['word']}\n"
        return res

    def __repr__(self):
        return self.__str__()
