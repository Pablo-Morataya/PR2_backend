from Usuario import Usuario

usuarios = [Usuario("Usuario", "Maestro", "Admin", "admin", "Administrador")]

class ControladorUsuario():

    def agregarUsuario(self, nombre, apellido, usuario, contrasenia, tipo):
        global usuarios
        condicion = self.comprobarExistencia(usuario)
        if condicion == False:
            nuevo_usuario =  Usuario(nombre, apellido, usuario, contrasenia, tipo)
            usuarios.append(nuevo_usuario)
            return True
        elif condicion == True:
            return False

    def comprobarExistencia(self, usuario):
        global usuarios
        for apun in usuarios: 
            if apun.usuario != usuario:
                return False
            elif apun.usuario == usuario:
                return True
        return False

    def obtenerUsuarios(self):
        global usuarios
        return usuarios