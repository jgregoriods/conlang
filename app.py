from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.language import Language, parse_vocabulary
from src.vocabulary import Vocabulary
from src.sound_change import SoundChange
import os
import re
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
    with open(f'static/languages/{language_id}_vocabulary.json', 'r') as f:
        language.vocabulary = Vocabulary.from_json(json.load(f))
    return render_template('language.html', language=language, vocabulary=language.vocabulary)


@app.route('/languages/create', methods=['GET', 'POST'])
def create_language():
    if request.method == 'POST':
        phonemes = {}
        for i in range(1, 6):
            if f'C{i}' in request.form:
                phonemes[f'C{i}'] = request.form[f'C{i}'].split()
            if f'V{i}' in request.form:
                phonemes[f'V{i}'] = request.form[f'V{i}'].split()
        patterns = [pattern for pattern in request.form['patterns'].split()]
        for i in range(len(patterns)):
            patterns[i] = re.sub(r'(\d+)', r'\1 ', patterns[i]).strip()
        stress = [int(i) for i in  request.form.getlist('stress')]

        language = Language(phonemes, patterns, stress)
        language.generate_vocabulary()

        path = f'languages/{language.id}.json'
        path = os.path.join(app.static_folder, path)
        with open(path, 'w') as f:
            json.dump(language.to_json(), f)

        path = f'languages/{language.id}_vocabulary.json'
        path = os.path.join(app.static_folder, path)
        with open(path, 'w') as f:
            json.dump(language.vocabulary.to_json(), f)

        conlang = Conlang(language_id=language.id)
        db.session.add(conlang)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/mutate/<language_id>', methods=['GET', 'POST'])
def mutate(language_id):
    if request.method == 'GET':
        return render_template('mutate.html', language_id=language_id)

    elif request.method == 'POST':
        if request.form.get('random_mutation'):
            sc = SoundChange(tonogenesis=request.form.get('tonogenesis'))
        else:
            pipeline = request.form.getlist('sound_changes')
            sc = SoundChange(pipeline, tonogenesis=request.form.get('tonogenesis'))
        replacement_rate = float(request.form['replacement_rate']) / 100
        with open(f'static/languages/{language_id}.json', 'r') as f:
            language = Language.from_json(json.load(f))
        with open(f'static/languages/{language_id}_vocabulary.json', 'r') as f:
            language.vocabulary = Vocabulary.from_json(json.load(f))
        new_vocabulary = language.mutate(sc, replacement_rate)
        language_specs = parse_vocabulary(new_vocabulary)
        new_language = Language(**language_specs)
        new_vocabulary.id = language.id

        # cleanup
        files_to_remove = os.listdir(os.path.join(app.static_folder, 'temp'))
        for file in files_to_remove:
            os.remove(os.path.join(app.static_folder, 'temp', file))
        
        path = f'temp/{new_language.id}.json'
        path = os.path.join(app.static_folder, path)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_language.to_json(), f)

        path = f'temp/{new_language.id}_vocabulary.json'
        path = os.path.join(app.static_folder, path)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(new_vocabulary.to_json(), f)

        return render_template('mutate.html',
                               language_id=language_id,
                               old_language=language,
                               old_vocabulary=language.vocabulary,
                               new_vocabulary=new_vocabulary,
                               new_language_id=new_language.id)


@app.route('/save/<language_id>')
def save(language_id):
    os.rename(f'static/temp/{language_id}.json', f'static/languages/{language_id}.json')
    os.rename(f'static/temp/{language_id}_vocabulary.json', f'static/languages/{language_id}_vocabulary.json')

    conlang = Conlang(language_id=language_id)
    db.session.add(conlang)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete_language/<language_id>', methods=['POST'])
def delete_language(language_id):
    language = Conlang.query.filter_by(language_id=language_id).first()
    db.session.delete(language)
    db.session.commit()
    os.remove(f'static/languages/{language_id}.json')
    os.remove(f'static/languages/{language_id}_vocabulary.json')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
