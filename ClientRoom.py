import sys 
import Ice 
import os
import json
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ClientRoom(Ice.Application): 

    def elegirOpcion(self):
        print("Que quiere hacer:\n1.Publicar\n 2.Remover ")
        op= int(input("Elija un numero>"))
        return op

    def run (self,argv):
        broker=self.communicator()
        proxy_RoomManager = broker.stringToProxy(argv[1])
        RoomManager = IceGauntlet.RoomManagerPrx.checkedCast(proxy_RoomManager)
        token = argv[2]
        roomData = str(argv[3])
        if not RoomManager:
            raise RuntimeError('Invalid Proxy')
        
        option = self.elegirOpcion()

        if option == 1:
            
            try:
                
                with open(roomData) as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                print("llega aqui")
                RoomManager.publish(str(token),str(datos_usuario))
        elif option == 2:
            print("llego aqui")
            try:
                with open(roomData) as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                print("y aqui")
                roomData=datos_usuario["room"]
                print(roomData)
                RoomManager.remove(str(token),str(roomData))
                
        

        
ClientRoom().main(sys.argv)  