import sys 
import Ice 
import os
import json
import argparse
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ClientRoom(Ice.Application): 
    def argumentos(self):
        parser = argparse.ArgumentParser(description='Proxy, user  y elegir una opcion: 1.Publish 2.Remove')
        parser.add_argument("-p","--proxy",required=True, help='proxy',type=str)
        parser.add_argument("-t","--token",required=True,help='token',type=str)
        parser.add_argument("-f","--file",required=True,help='file json',type=str)
        parser.add_argument("-o","--option",required=True,help='1.Publish 2.Remove',type=str)
        

        args=parser.parse_args()
        return args

    def run (self,argv):
        args = self.argumentos()
        proxy=args.proxy
        token=args.token
        roomData=str(args.file)
        option=args.option
        broker=self.communicator()
        proxy_RoomManager = broker.stringToProxy(proxy)
        
        RoomManager=IceGauntlet.RoomManagerPrx.checkedCast(proxy_RoomManager)
        
        if not RoomManager:
            raise RuntimeError('Invalid Proxy')

        if option == "1":
            
            try:
                
                with open(roomData) as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                RoomManager.publish(str(token),str(datos_usuario))
        elif option == "2":
            try:
                with open(roomData) as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                roomData=datos_usuario["room"]
                RoomManager.remove(str(token),str(roomData))
                    
ClientRoom().main(sys.argv)  