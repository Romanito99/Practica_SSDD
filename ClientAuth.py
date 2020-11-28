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

    def solicitarContraseña(self):
        print("Introduzca una new_hash para el usuario")
        new_hash = getpass.getpass("Contraseña>")
        new_hash= self.computeHash(new_hash)
        return new_hash

    def solicitarUsuario(self):
        print("Escriba el nombre del usuario")
        user = str(input("Usuario>"))
        return user
        
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
            new_hash = self.solicitarContraseña()
            nombre_usuario=datos_usuario[user]
            
            if(len(nombre_usuario)==0):
                print("hola")
                authserver.changePassword(user, None ,new_hash)
            else:   
                current_hash = nombre_usuario["password_hash"]
                authserver.changePassword(user, current_hash ,new_hash)

 

ClientAuth().main(sys.argv)
 