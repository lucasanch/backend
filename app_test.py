
def saludar(nombre, signo = "!"):

    print(f'Hola {nombre}{signo}')

saludar("alumnos", "")

mi_diccionario = {'a': 1, 'b': 2, 'c': 3}

del mi_diccionario['b']

print(mi_diccionario)

mi_numero = 5

mi_numero = int(input("Ingrese un dígito"))

print(mi_numero)

# importamos el framework Flask
from flask import Flask

    # importamos la funcion que nos permite el render de los templates
from flask import render_template

    # creamos la aplicacion
app = Flask(__name__)

    # proporcionamos la ruta a la raiz del sitio
@app.route('/')
def index():
        # devolvemos codigo html para ser renderizado
        return "<h1>Hola desde Flask!</h1>"


# estas lineas de codigo las requiere  python para q se pueda empezar a trabajar con la aplicacion
if __name__=='__main__':
        # corremos la aplicacion en modo debug
        app.run(debug=True)


