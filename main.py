from flask import Flask, render_template, request, flash
from flask.helpers import url_for
from werkzeug.utils import redirect
from datetime import datetime
from flaskext.mysql import MySQL

# Instanciamos un objeto Flask
app = Flask(__name__)

# Creamos clave secreta
app.secret_key = 'clave_secreta_flask'

# Conexion a MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'proyectoFlask'

mysql = MySQL()
mysql.init_app(app)


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

@app.route('/crear-coche', methods=['GET', 'POST'])
def crear_coche():
    if request.method == 'POST':
        # Creamos nuestras variables que luego los pasaremos a la consulta para guardarlo
        # en nuestra base de datos.
        modelo = request.form['model']
        marca = request.form['mark']
        precio = request.form['price']
        ciudad = request.form['city']

        
        cursor = mysql.get_db().cursor()
        # Consulta
        cursor.execute("INSERT INTO coches VALUES(NULL, %s, %s, %s, %s)", ( marca, modelo, precio, ciudad))
        # Mensaje Flash
        flash('Se ha añadido el auto correctamente')
        return redirect(url_for('coches'))
        
    return render_template('crear_coche.html')

@app.route('/coches')
def coches():
    # Creamos el cursor
    cursor = mysql.get_db().cursor()

    # Realizamos una consulta a la base de datos
    cursor.execute("SELECT * FROM coches ORDER BY id DESC")

    # Sacamos toda la informacion que hay dentro de la tabla
    coches = cursor.fetchall()
    cursor.close()

    return render_template('coches.html', coches=coches)

@app.route('/coche/<coche_id>')
def coche(coche_id):
    # Creamos el cursor
    cursor = mysql.get_db().cursor()

    # Realizamos una consulta a la base de datos
    cursor.execute("SELECT * FROM coches WHERE id = %s", (coche_id))

    # Sacamos toda la informacion que hay dentro de la tabla
    coche = cursor.fetchall()
    cursor.close()

    return render_template('coche.html', coche=coche[0])

@app.route('/borrar-coche/<coche_id>')
def borrar_coche(coche_id):
    # Creamos el cursor
    cursor = mysql.get_db().cursor()

    # Realizamos una consulta a la base de datos
    cursor.execute("DELETE FROM coches WHERE id = %s", (coche_id))

    flash('El coche ha sido eliminado correctamente')

    return redirect(url_for('coches'))

@app.route('/editar-coche/<coche_id>', methods=['GET', 'POST'])
def editar_coche(coche_id):

    if request.method == 'POST':
        modelo = request.form['model']
        marca = request.form['mark']
        precio = request.form['price']
        ciudad = request.form['city']

        
        cursor = mysql.get_db().cursor()
        # Consulta
        cursor.execute("""
                        UPDATE coches 
                        SET modelo = %s, 
                        marca = %s, 
                        precio = %s, 
                        localidad = %s 
                        WHERE id = %s
                    """, ( marca, modelo, precio, ciudad, coche_id))

        # Mensaje Flash
        flash('Se ha editado el coche correctamente')

        return redirect(url_for('coche', coche_id=coche_id))
    else:
        # Creamos el cursor
        cursor = mysql.get_db().cursor()

        # Realizamos una consulta a la base de datos
        cursor.execute("SELECT * FROM coches WHERE id = %s", (coche_id))

        # Sacamos toda la informacion que hay dentro de la tabla
        coche = cursor.fetchall()
        cursor.close()

        return render_template('crear_coche.html', coche=coche[0])

if __name__ == '__main__':
    app.run(debug=True)