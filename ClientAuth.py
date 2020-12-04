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
        print("Introduzca su  contraseña")
        hash = getpass.getpass("Contraseña>")
        hash= self.computeHash(hash)
        return hash

    def solicitarUsuario(self):
        print("Escriba el nombre del usuario")
        user = str(input("Usuario>"))
        return user
        
    def elegirOpcion(self):
        print("Que quiere hacer:\n0.Autenticarse\n1.Cambiar tu contraseña\n 2. Obtener un nuevo token ")
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
                new_hash = self.solicitarNuevaContraseña()
                authserver.changePassword(str(user),None,str(new_hash))
                print('"{}"'.format(nombre_usuario["current_token"]), flush=True)
                
            else:
                hash = self.solicitarContraseña()
                current_hash = nombre_usuario["password_hash"]
                print(isinstance(hash,str))
                opcion = self.elegirOpcion
                if current_hash == hash  :
                    print("Usuario correcto\n ")
                    opcion = self.elegirOpcion()
                    if opcion == 1:
                        new_hash = self.solicitarNuevaContraseña()
                        authserver.changePassword(user, current_hash ,new_hash)
                        print('"{}"'.format(nombre_usuario["current_token"]), flush=True)
                    elif opcion == 2:
                        token=authserver.getNewToken(user,current_hash)
                        print('"{}"'.format(nombre_usuario["current_token"]), flush=True)
                    elif opcion == 0: 
                        print('"{}"'.format(nombre_usuario["current_token"]), flush=True)
                else:
                    print("El usuario introducizo no existe o su contraseña es incorerecta\n ")

       
            
            
           
                                
                
            

ClientAuth().main(sys.argv)
 