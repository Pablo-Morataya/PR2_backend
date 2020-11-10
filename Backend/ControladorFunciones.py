from Funcion import Funcion
import pytz
import datetime

funciones = []

class ControladorFunciones():

    def agregarFuncion(self, pelicula, sala, hora, estado):
        global funciones
        if estado == True:
            nueva_funcion = Funcion(pelicula, sala, hora, "Disponible")
            funciones.append(nueva_funcion)
        elif estado == False:
            nueva_funcion = Funcion(pelicula, sala, hora, "NO Disponible")
            funciones.append(nueva_funcion)
    
    def retornarFunciones(self):
        global funciones
        return funciones
    
    def disponible(self, horaAc):
        timezone = pytz.timezone('America/Guatemala')
        fecha_completa = datetime.datetime.now(tz=timezone)
        hora = fecha_completa.strftime("%H")
        minutos = fecha_completa.strftime("%M")
        hora_actual = int(hora)
        min_actual = int(minutos)
        tiempo_funcion = horaAc.split(":")
        hora_funcion = int(tiempo_funcion[0])
        min_funcion = int(tiempo_funcion[1])
        if hora_actual > hora_funcion:
            return False
        elif hora_actual == hora_funcion:
            if min_actual > min_funcion:
                return False
        return True