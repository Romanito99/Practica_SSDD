import sys 
import Ice 
import os
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib
import json
import getpass

class ClientAuth(Ice.Application): 
    def computeHash(self,filename):
        fileHash = hashlib.sha256()
        fileHash.update(filename.encode())
        return fileHash.hexdigest()

    def solicitarNuevaContraseña(self):
        print("Introduzca su nueva contraseña  para el usuario")
        new_hash = getpass.getpass("Contraseña>")
        new_hash= self.computeHash(new_hash)
        return new_hash
    def solicitarContraseña(self):
        print("Introduzca su  contraseña. Si es un usuario vacio no escriba nada  ")
        hash = getpass.getpass("Contraseña>")
        hash= self.computeHash(new_hash)
        return hash

    def solicitarUsuario(self):
        print("Escriba el nombre del usuario")
        user = str(input("Usuario>"))
        return user
        
    def elegirOpcion(self):
        print("Que quiere hacer:\n1.Cambiar tu contraseña\n 2. Obtener un nuevo token ")
        op= int(input("Elija un numero>"))
        return op
        
    def run(self, argv):
        broker=self.communicator()
        proxy_authserver=broker.stringToProxy(argv[1])
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy_authserver)

        
        #authserver.getNewToken("cesar.braojos",new_hash)

        if not authserver:
            raise RunTimeError('Invalid Proxy')
        
        try:
            with open("users.json") as f:
                datos_usuario=f.read()
                
            datos_usuario=json.loads(datos_usuario)
            
        except:
            print("No se ha podido leer el fichero json de busqueda")

        else:
            user = self.solicitarUsuario()

            nombre_usuario = datos_usuario[user]       
            if(len(nombre_usuario)==0):
                print("")
                new_hash = self.solicitarNuevaContraseña()
                authserver.changePassword(user , None ,new_hash)
            else:
                hash = self.solicitarContraseña()
                current_hash = nombre_usuario["password_hash\n "]
                opcion = self.elegirOpcion
                if current_hash == hash  :
                print("Usuario correcto\n ")
                    if opcion == 1:
                    new_hash = self.solicitarNuevaContraseña()
                    authserver.changePassword(user, current_hash ,new_hash)
                    elif opcion == 2:
                        token=authserver.getNewToken(user,current_hash)
                    else 
                    print("El usuario introducizo no existe o su contraseña es incorerecta\n ")

       
            print("El  nuevo token es: ",token)
            
           
                                
           


ClientAuth().main(sys.argv)