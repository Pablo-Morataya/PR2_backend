import pytz
import datetime

class Funcion():
    def __init__(self, pelicula, sala, hora, estado):
        self.pelicula = pelicula
        self.sala = sala
        self.hora = hora
        self.estado = estado
        self.lugares = ["vacio","vacio","vacio","vacio","vacio","vacio","vacio","vacio","vacio"]