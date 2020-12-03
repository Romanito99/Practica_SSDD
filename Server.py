import sys
import os
import json
import ast
import random
import glob
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ServerI(IceGauntlet.Server):

    '''Clase ServerI'''
    def __init__(self,authserver):
        self.authserver=authserver

    def publish(self , token , room_data , current=None):
        print("hola")
        ''' hola '''
        
        if True:
            fichero=ast.literal_eval(room_data)
            try:
                
                data=fichero["data"]
                room=fichero["room"]
            except Exception as error:
                print ("Error {}".format(error))
                raise IceGauntlet.WrongRoomFormat(str(error))
            else:
                
                lista=glob.glob(os.path.join('mapas','*.json'))
                
                for i in lista:
                    print(str(i))
                    with open(str(i))as fichero_mapas:
                        datos_mapa=fichero_mapas.read()
                    datos_mapa=json.loads(datos_mapa)
                    print(datos_mapa)
                    if datos_mapa["data"] == fichero["data"]:
                        print ("Error al comprobar {}".format("la excepcion Unauthorized"))
                        raise IceGauntlet.RoomAlreadyExists("Este fichero ya existe ")

                #random=random.randrandge(0,1000000)    
                with open(("mapas/leveljson"),"w") as fichero_mapas:
                    json.dump(fichero, fichero_mapas)

                with open("mapas.json") as fichero_mapas:
                    c=fichero_mapas.read()
                mapas=json.loads(c)
                mapas[fichero["room"]]={}
                mapas[fichero["room"]]["current_token"]=token
                

            with open('mapas.json', 'w') as contents:
                json.dump(mapas, contents, indent=2, sort_keys=True)
        else:
            print ("Error al comprobar {}".format("la excepcion Unauthorized"))
            raise IceGauntlet.Unauthorized(str("la excepcion"))

    def remove(self , token , roomName , current=None):
        '''hola'''
        if True:
            with open("mapas.json") as fichero_mapas:
                c=fichero_mapas.read()
            mapas=json.loads(c)
            lista=glob.glob(os.path.join('hola','*.json'))
            q = random.randrange(1,len(lista))
            for i in lista:
                mapa=str(i)
                try:
                    with open(mapa) as fichero_mapas:
                        datos_mapa=fichero_mapas.read()
                    datos_mapa=json.loads(datos_mapa)
                                    
                    if mapas[roomName] == roomName & datos_mapa["room"] == roomName:
                        if mapas[roomName]["current_token"]==token:
                            mapas.pop(roomName)
                            os.remove(mapa)
                            with open("mapas.json","w") as fichero_mapas:
                                json.dump(mapas,fichero_mapas, indent=2, sort_keys=True)
                except Exception as error:
                    raise IceGauntlet.RoomNotExists("Este mapa no existe")
                    
        else:
            print ("Error al comprobar {}".format("la excepcion"))
            raise IceGauntlet.Unauthorized(str("la excepcion"))

    

class DungeonI(IceGauntlet.Dungeon):
    def getRoom(self,current=None):
        print("hola")
        '''Este metodo es para obtener un mapa'''                     
        
        try: 
            lista=glob.glob(os.path.join('hola','*.json'))
            q = random.randrange(1,len(lista))
            ruta=(lista.pop(q))
            with open(str(ruta)) as fichero_mapas:
                datos_usuario=fichero_mapas.read()
            datos_usuario=json.loads(datos_usuario)
        except Exception as error:
            raise IceGauntlet.RoomNotExists("El servidor no tiene ningun mapa") 
        return str(datos_usuario)

    
class Server(Ice.Application):
    '''Clase server '''
    def run(self, argv):
        proxy=self.communicator().stringToProxy(argv[1])
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not authserver:
            raise RunTimeError('Invalid Proxy')
        servant=ServerI(authserver)
        adapter = self.communicator().createObjectAdapter('ServerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('server'))
        print('"{}"'.format(proxy), flush=True)
        adapter.activate()
        
        servant_juego=DungeonI()
        adapter_dungeon = self.communicator().createObjectAdapter('DungeonAdapter')
        proxy_dungeon = adapter.add(servant_juego, self.communicator().stringToIdentity('dungeon'))
        print('"{}"'.format(proxy_dungeon), flush=True)
        adapter_dungeon.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0

Server().main(sys.argv)