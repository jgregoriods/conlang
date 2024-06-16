from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.language import Language
from src.vocabulary import Vocabulary
from src.sound_change import SoundChange
import os
import json


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conlang.db'
# app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Conlang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.String)


#with app.app_context():
#    db.drop_all()
#    db.create_all()
#    db.session.commit()


@app.route('/')
def index():
    languages = Conlang.query.all()
    return render_template('index.html', languages=languages)


@app.route('/languages/<language_id>')
def languages(language_id):
    with open(f'static/languages/{language_id}.json', 'r') as f:
        language = Language.from_json(json.load(f))
    with open(f'static/vocabularies/{language_id}.json', 'r') as f:
        language.vocabulary = Vocabulary.from_json(json.load(f))
    return render_template('language.html', language=language, vocabulary=language.vocabulary)


@app.route('/languages/create', methods=['GET', 'POST'])
def create_language():
    if request.method == 'POST':
        consonants = request.form['consonants']
        vowels = request.form['vowels']
        phonemes = {'C': consonants.split(), 'V': vowels.split()}
        patterns = [pattern for pattern in request.form['patterns'].split(',')]
        stress = [int(i) for i in request.form['stress'].split()]

        language = Language(phonemes, patterns, stress)
        language.generate_vocabulary()

        path = f'languages/{language.id}.json'
        path = os.path.join(app.static_folder, path)
        with open(path, 'w') as f:
            json.dump(language.to_json(), f)

        path = f'vocabularies/{language.id}.json'
        path = os.path.join(app.static_folder, path)
        with open(path, 'w') as f:
            json.dump(language.vocabulary.to_json(), f)

        conlang = Conlang(language_id=language.id)
        db.session.add(conlang)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/sound_change/<language_id>', methods=['POST'])
def sound_change(language_id):
    rule = request.form['sound_change']
    with open(f'static/languages/{language_id}.json', 'r') as f:
        language = Language.from_json(json.load(f))
    with open(f'static/vocabularies/{language_id}.json', 'r') as f:
        language.vocabulary = Vocabulary.from_json(json.load(f))
    sc = SoundChange([rule])
    new_vocabulary = language.mutate(sc)
    print(new_vocabulary)
    return redirect(url_for('languages', language_id=language_id, mutated=new_vocabulary))


@app.route('/delete_language/<language_id>', methods=['POST'])
def delete_language(language_id):
    language = Conlang.query.filter_by(language_id=language_id).first()
    db.session.delete(language)
    db.session.commit()
    os.remove(f'static/languages/{language_id}.json')
    os.remove(f'static/vocabularies/{language_id}.json')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
