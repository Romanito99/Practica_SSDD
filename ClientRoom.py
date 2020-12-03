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
        proxy_server = broker.stringToProxy(argv[1])
        server = IceGauntlet.ServerPrx.checkedCast(proxy_server)
        token = argv[2]
        roomData = str(argv[3])
        if not server:
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
                server.publish(str(token),str(datos_usuario))
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
                server.remove(str(token),str(roomData))
                
        

        
ClientRoom().main(sys.argv)  