import pytz
import datetime

class Pelicula():
    def __init__ (self, nombre, url, puntuacion, duracion, sinopsis, hora):
        self.nombre = nombre
        self.url = url
        self.puntuacion = puntuacion
        self.duracion = duracion
        self.sinopsis = sinopsis
        self.hora = hora
        self.resenias = []

    def disponible(self):
        timezone = pytz.timezone('America/Guatemala')
        fecha_completa = datetime.datetime.now(tz=timezone)
        hora = fecha_completa.strftime("%H")
        minutos = fecha_completa.strftime("%M")
        hora_actual = int(hora)
        min_actual = int(minutos)
        tiempo_funcion = self.hora.split(":")
        hora_funcion = int(tiempo_funcion[0])
        min_funcion = int(tiempo_funcion[1])
        if hora_actual > hora_funcion:
            return False
        elif hora_actual == hora_funcion:
            if min_actual > min_funcion:
                return False
        return True