from flask import Flask, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
from datetime import datetime

# Instanciamos un objeto Flask
app = Flask(__name__)

# Context processors
@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }
#Endpoints

#Creamos una ruta
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/information')
@app.route('/information/<string:name>')
@app.route('/information/<string:name>/<string:lastName>')
def information(name = None, lastName = None):
    text = ""
    if name != None and lastName != None:
        text = f"Bienvenido, {name} {lastName}"

    return render_template('information.html', text=text)

@app.route('/contact')
@app.route('/contact/<redireccion>')
def contact(redireccion = None):

    if redireccion is not None:
        return redirect(url_for('lenguage'))

    return render_template('contact.html')

@app.route('/lenguage')
def lenguage():
    languages = ['HTML', 'CSS', 'Python', 'Javascript', 'C', 'Java']

    return render_template('language.html', languages=languages)

if __name__ == '__main__':
    app.run(debug=True)