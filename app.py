from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.language import Language

import json


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conlang.db'
# app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class LanguageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phonemes = db.Column(db.String(50), nullable=False)
    patterns = db.Column(db.String(50), nullable=False)
    stress = db.Column(db.String(50), nullable=False)


class VocabularyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    definition = db.Column(db.String(200), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('language_model.id'), nullable=False)


# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     db.session.commit()


@app.route('/')
def index():
    languages = LanguageModel.query.all()
    return render_template('index.html', languages=languages)


@app.route('/languages/<int:language_id>')
def languages(language_id):
    language = LanguageModel.query.get(language_id)
    vocabulary = VocabularyModel.query.filter_by(language_id=language_id).all()
    return render_template('language.html', language=language, vocabulary=vocabulary)


@app.route('/languages/create', methods=['GET', 'POST'])
def create_language():
    if request.method == 'POST':
        consonants = request.form['consonants']
        vowels = request.form['vowels']
        phonemes = {'C': consonants.split(), 'V': vowels.split()}
        patterns = [list(pattern) for pattern in request.form['patterns'].split()]
        stress = [int(i) for i in request.form['stress'].split()]

        language = Language(phonemes, patterns, stress)
        language.generate_vocabulary()

        language_model = LanguageModel(phonemes=json.dumps(phonemes), patterns=json.dumps(patterns), stress=json.dumps(stress))
        db.session.add(language_model)
        db.session.commit()
        
        for item in language.vocabulary.items:
            word = item['word']
            definition = item['definition']
            vocabulary_model = VocabularyModel(word=word, definition=definition, language_id=language_model.id)
            db.session.add(vocabulary_model)
            db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/sound_change', methods=['POST'])
def sound_change():
    pass


if __name__ == '__main__':
    app.run(debug=True)
