import sys 
import Ice 
import os
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
        roomData = argv[3]
        if not server:
            raise RuntimeError('Invalid Proxy')
        
        opcion = self.elegirOpcion

        if option == 1:
            try :
                try:
                    with open("juego/assets/level_2.json") as f:
                        datos_usuario=f.read()
                    datos_usuario=json.loads(datos_usuario)
                except:
                    print("No se ha podido leer el fichero json de busqueda")
                else:
                    room_data = (room) 
                    
                    
            
            server.publish(token,datos_usuario)
        if option == 2:
            server.remove(token,roomData)

        

        
       