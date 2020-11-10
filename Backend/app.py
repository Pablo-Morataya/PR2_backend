from flask import Flask, request, jsonify
import json
from flask_cors import CORS, cross_origin
from Peliculas import Pelicula
from Funcion import Funcion
from ControladorUsuarios import ControladorUsuario
from ControladorFunciones import ControladorFunciones
import os

a = ControladorUsuario()
b = ControladorFunciones()

app = Flask(__name__)
# CORS ALLOW
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)

#-------------------------
peliculas = []
funciones = b.retornarFunciones()
pelicula_actual = None
confirm = True
#-------------------------
#-------------------------
usuarios = a.obtenerUsuarios()
usuario_actual = None
#-------------------------

#PELICULASS
@app.route('/', methods = ['GET'])
@cross_origin()
def inicio():
    return "Bienvenido"

@app.route('/agregarPeliculas', methods=['POST'])
def agregarPeliculas():
    datos = request.get_json()
    nombre = datos['nombre']
    url = datos['url']
    puntuacion = datos['puntuacion']
    duracion = datos['duracion']
    sinopsis = datos['sinopsis']
    hora = datos['hora']
    nueva_pelicula = Pelicula(nombre, url, puntuacion, duracion, sinopsis,hora)
    global peliculas
    peliculas.append(nueva_pelicula)
    return jsonify({
        'status': 200,
        'mensaje': 'Se agrego la pelicula'
    })

@app.route('/agregarPeliculasMasivas', methods=['POST'])
def agregarPeliculasMasivass():
    datos = request.get_json()

    carga = datos['archivos']

    for apun in carga:
        aux = apun.split(",")
        nombre = aux[0]
        url = aux[1]
        puntuacion = aux[2]
        duracion = aux[3]
        sinopsis = aux[4]
        hora = "NO espeficicado"
        nueva_pelicula = Pelicula(nombre, url, puntuacion, duracion, sinopsis, hora)
        global peliculas
        peliculas.append(nueva_pelicula)
    return jsonify({
            'status': 200,
            'mensaje': 'Peliculas cargadas'
    })

@app.route('/obtenerPeliculas', methods = ['GET'])
@cross_origin()
def obtenerPeliculas():
    json_peliculas = []
    global peliculas
    for pelicula in peliculas:
        json_peliculas.append({"nombre":pelicula.nombre, "url":pelicula.url, "sinopsis": pelicula.sinopsis, "hora":pelicula.hora, "duracion":pelicula.duracion, "puntuacion":pelicula.puntuacion}) 
    return jsonify(json_peliculas)

@app.route('/agregarPeliculaActual', methods = ['POST'])
@cross_origin()
def agregarPeliculaActual():
    datos = request.get_json()
    nombre = datos['nombre']
    global peliculas
    for pelicula in peliculas:
        if pelicula.nombre == nombre:
            global pelicula_actual
            pelicula_actual = pelicula
            return jsonify({
                'status': 200
            })

@app.route('/obtenerPeliculaActual', methods = ['GET'])
@cross_origin()
def obtenerPeliculaActual():
    global pelicula_actual
    return jsonify({
            'status': 400,
            'nombre':pelicula_actual.nombre, 
            'url':pelicula_actual.url, 
            'sinopsis': pelicula_actual.sinopsis, 
            'hora':pelicula_actual.hora, 
            'duracion':pelicula_actual.duracion, 
            'puntuacion':pelicula_actual.puntuacion,
            'resenias':pelicula_actual.resenias
    })

@app.route('/agregarReseñas', methods = ['POST'])
@cross_origin()
def agregarResenias():
    datos = request.get_json()
    nombre = datos['nombre']
    resenia = datos['resenias']
    global peliculas
    global usuario_actual
    for pelicula in peliculas:
        if pelicula.nombre == nombre:
            pelicula.resenias.append(usuario_actual.usuario + "," + resenia)
            return jsonify({
                'status': 200,
                'mensaje': 'Reseña agregada'
                })
    return jsonify({
        'status': 404,
        'mensaje': 'No existe esa película'
            })

@app.route('/obtenerResenias', methods = ['POST'])
@cross_origin()
def obtenerResenias():
    json_peliculas = []
    datos = request.get_json()
    nombre = datos['nombre']
    global peliculas
    for pelicula in peliculas:
        if pelicula.nombre == nombre:
            if pelicula.resenias == None:
                return jsonify({
                    'status': 404,
                    'mensaje': "Sin reseñas"
                    })
            elif pelicula.resenias != None: 
                json_peliculas.append({"nombre":pelicula.nombre, "url":pelicula.url, "reseñas":pelicula.resenias})
                return jsonify(json_peliculas)
    return jsonify({
        'status': 400,
        'mensaje': 'No existe esa película'
    })

@app.route('/agregarFuncion', methods = ['POST'])
@cross_origin()
def agregarFuncion():
    datos = request.get_json()
    nombre = datos['nombre']
    sala = datos['sala']
    hora = datos['hora']
    global peliculas
    for apunt in peliculas:
        if apunt.nombre == nombre:
            b.agregarFuncion(apunt.nombre, sala, hora, b.disponible(hora))
            global funciones
            funciones = b.retornarFunciones()
            return jsonify({
                'status': 200,
                'mensaje': 'Función agregada'
                })
    return jsonify({
        'status': 400,
        'mensaje': 'Película Inexistente'
        })
    
@app.route('/eliminarFuncion', methods = ['DELETE'])
@cross_origin()
def eliminarFuncion():
    datos = request.get_json()
    nombre = datos['pelicula']
    global funciones
    for apun in funciones:
        if apun.pelicula == nombre:
            funciones.remove(apun)
            return jsonify({
                'status': 200,
                'mensaje': 'Pelicula eliminada'
                })
    
@app.route('/eliminarPeliculas', methods = ['DELETE'])
@cross_origin()
def eliminarPeliculas():
    datos = request.get_json()
    nombre = datos['nombre']
    global peliculas
    for apun in peliculas:
        if apun.nombre == nombre:
            peliculas.remove(apun)
    return jsonify({
            'status': 200,
            'mensaje': 'Pelicula eliminada'
        })   

@app.route('/obtenerFunciones', methods = ['GET'])
@cross_origin()
def obtenerFunciones():
    json_funciones = []
    global funciones
    for funcion in funciones:
        json_funciones.append({"pelicula":funcion.pelicula, "sala":funcion.sala, "hora":funcion.hora, "estado":funcion.estado, "lugares":funcion.lugares})   
    return jsonify(json_funciones)

@app.route('/asistirFuncion', methods = ['POST'])
@cross_origin()
def asistirFuncion():
    datos = request.get_json()
    nombre = datos['pelicula']
    posicion = datos['lugar']
    global funciones
    for funcion in funciones:
        if funcion.pelicula == nombre:
            funcion.lugares[posicion] = "lleno"
            return jsonify({'status':200})
    return jsonify({'status': 400})

#------------------------------ USUARIOOOS  ---------------------------------
@app.route('/obtenerUsuarios', methods = ['GET'])
@cross_origin()
def obtenerUsuarios():
    json_usuarios = []
    global usuarios
    for puntero in usuarios:
        json_usuarios.append({"nombre":puntero.nombre, "apellido":puntero.apellido, "usuario":puntero.usuario, "tipo":puntero.tipo})
    return jsonify(json_usuarios)

@app.route('/agregarUsuariosCliente', methods = ['POST'])
@cross_origin()
def agregarUsuarios():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']
    usuario = datos['usuario']
    password = datos['password']
    confirm = datos['confirm']
    tipo = "Cliente"
    global a
    if password == confirm: 
        if a.comprobarExistencia(usuario) == True:
            return jsonify({
                'status': 404,
                'mensaje': 'Existe un usuario con ese nombre de usuario'
            })
        elif a.comprobarExistencia(usuario) == False:
            global usuarios
            a.agregarUsuario(nombre, apellido, usuario, password, tipo)
            usuarios = a.obtenerUsuarios()
            for pun in usuarios:
                print(pun.nombre)       
    elif password != confirm:
        return jsonify({
            'status': 400,
            'mensaje': 'Las contraseñas no coinciden'
        })
    
    return jsonify({
        'status': 200,
        'mensaje': 'Usuario agregado'
    })

@app.route('/agregarUsuariosAdmin', methods = ['POST'])
@cross_origin()
def agregarUsuariosAdmin():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']
    usuario = datos['usuario']
    password = datos['password']
    confirm = datos['confirm']
    tipo = "Administrador"
    global a
    if password == confirm: 
        if a.comprobarExistencia(usuario) == True:
            return jsonify({
                'status': 404,
                'mensaje': 'Existe un usuario con ese nombre de usuario'
                })
        elif a.comprobarExistencia(usuario) == False:
            global usuarios
            a.agregarUsuario(nombre, apellido, usuario, password, tipo)
            usuarios = a.obtenerUsuarios() 
    elif password != confirm:
        return jsonify({
            'status': 400,
            'mensaje': 'Las contraseñas no coinciden'
            })
    return jsonify({
        'status': 200,
        'mensaje': 'Usuario agregado'
        })

@app.route('/ingresar', methods = ['POST'])
@cross_origin()
def ingresar():
    datos = request.get_json()
    usuario = datos['usuario']
    password = datos['password']
    global a
    global usuarios
    for puntero in usuarios:
        if (puntero.usuario == usuario) and (puntero.contrasenia == password):
            global usuario_actual
            usuario_actual = puntero
            global confirm 
            confirm == True
            return jsonify({
                'status': 200,
                'mensaje': 'Bienvenido',
                'tipo': puntero.tipo
                })
        elif (puntero.usuario == usuario) and (puntero.contrasenia != password):
            return jsonify({
                'status': 400,
                'mensaje': 'Contraseña incorrecta'
                })
    return jsonify({
        'status': 404,
        'mensaje': 'Usuario inexistente'
        })

@app.route('/obtenerActual', methods = ['GET'])
@cross_origin()
def obtenerActual():
    global usuario_actual
    if usuario_actual == None:
        return jsonify({
            'status': 400,
            'mensaje': 'Algo salio mal',
            })
    return jsonify({
        'status': 200,
        'nombre': usuario_actual.nombre,
        'apellido': usuario_actual.apellido,
        'usuario': usuario_actual.usuario,
        'password': usuario_actual.contrasenia,
        'confirm': usuario_actual.contrasenia
        })

@app.route('/modificarUsuario', methods = ['PUT'])
@cross_origin()
def modificarUsuario():
    datos = request.get_json()
    nombre = datos['nombre']
    apellido = datos['apellido']
    password = datos['password']
    confirm = datos['confirm']
    if password == confirm:
        global usuario_actual
        usuario_actual.nombre = nombre
        usuario_actual.apellido = apellido
        usuario_actual.contrasenia = password
        return jsonify({
        'status': 200,
        'mensaje': 'Se han guardado los cambios'
        })
    elif password != confirm:
        return jsonify({
            'status': 400,
            'mensaje': 'Las contraseñas no coinciden'
            })

#USUARIOOOS

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=puerto)