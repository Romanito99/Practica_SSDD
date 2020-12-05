import sys 
import Ice 
import os
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib
import json
import argparse
import getpass

class ClientAuth(Ice.Application): 
    def computeHash(self,filename):
        fileHash = hashlib.sha256()
        fileHash.update(filename.encode())
        return fileHash.hexdigest()

    def solicitarNuevaContraseña(self):
        print("Enter new password")
        new_hash = getpass.getpass("Enter password>")
        new_hash= self.computeHash(new_hash)
        return new_hash

    def solicitarContraseña(self):
        print("Enter password")
        hash = getpass.getpass("Enter password>")
        hash= self.computeHash(hash)
        return hash


    
    def argumentos(self):
        parser = argparse.ArgumentParser(description='Proxy, user  y elegir una opcion: 1.Cambiar contraseña 2.Cambiar el token')
        parser.add_argument("-p","--proxy",required=True, help='proxy',type=str)
        parser.add_argument("-u","--user",required=True,help='User',type=str)
        parser.add_argument("-o","--option",required=True,help='1.Para cambiar contraseña 2.Para cambiar el token',type=str)
        

        args=parser.parse_args()
        return args
        
    def run(self):
        args = self.argumentos()
        proxy=args.proxy
        user=args.user
        opcion=args.option
        broker=self.communicator()
        proxy_authserver=broker.stringToProxy(proxy)
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy_authserver)

        if not authserver:
            raise RunTimeError('Invalid Proxy')
        
        try:
            with open("users.json") as f:
                datos_usuario=f.read()
            datos_usuario=json.loads(datos_usuario)
        except:
            print("No se ha podido leer el fichero json de busqueda")

        else:
            
            nombre_usuario = datos_usuario[user]       
            if(len(nombre_usuario)==0):
                new_hash = self.solicitarNuevaContraseña()
                authserver.changePassword(str(user),None,str(new_hash))
                print('"{}"'.format(nombre_usuario["current_token"]), flush=True)
                
            else:
                hash = self.solicitarContraseña()
                current_hash = nombre_usuario["password_hash"]
                if current_hash == hash  :
                    print("Usuario correcto\n ")
                    if opcion == "1":
                        new_hash = self.solicitarNuevaContraseña()
                        authserver.changePassword(user, current_hash ,new_hash)
                        print('"{}"'.format(nombre_usuario["current_token"]), flush=True)
                    elif opcion == "2":
                        token=authserver.getNewToken(user,current_hash)

                        print('"{}"'.format(token), flush=True)
                    
                else:
                    print("El usuario introducizo no existe o su contraseña es incorerecta\n ")

ClientAuth().run()
 