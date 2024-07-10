
# importamos el framework Flask
from flask import Flask

# importamos la funcion que nos permite el render de los templates (los templates son todas la paginas html que vamos a utilia)
from flask import render_template

# creamos la aplicacion
app = Flask(__name__)

# proporcionamos la ruta a la raiz del sitio
@app.route('/')
def index():
    # devolvemos codigo html para ser renderizado
    return render_template('peliculas/index.html')

# estas lineas de codigo las requiere  python para q se pueda empezar a trabajar con la aplicacion

if __name__=='__main__':
    # corremos la aplicacion en modo debug
    app.run(debug=True)


#mysql = MySQL()

#app.config['MYSQL-DATABASE_HOST']= 'localhost'
#app.config['MYSQL-DATABASE_USER']= 'root'
#app.config['MYSQL-DATABASE_PASSWORD']= ''
#app.config['MYSQL-DATABASE_DB']= 'sistema1'

#mysql.init_app(app)