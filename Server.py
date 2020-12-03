import sys
import os
import json
import ast
import random
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
                print(room)
            except Exception as error:
                print ("Error {}".format(error))
                raise IceGauntlet.WrongRoomFormat(str(error))
            else:
                if os.path.isfile("icegauntlet/assets/"+fichero["room"]+"1.json"):
                    raise IceGauntlet.WrongRoomFormat("Este fichero ya existe ")
                else:
                    with open(("icegauntlet/assets/"+fichero["room"]+".json"),"w") as fichero_mapas:
                        json.dump(fichero, fichero_mapas)

                    with open("mapas.json") as fichero_mapas:
                        c=fichero_mapas.read()
                    mapas=json.loads(c)
                    print(fichero["room"])
                    mapas[fichero["room"]]={}
                    mapas[fichero["room"]]["current_token"]=token
                    mapas[fichero["room"]]["room"]=fichero["room"]

            with open('mapas.json', 'w') as contents:
                json.dump(mapas, contents, indent=2, sort_keys=True)
        else:
            print ("Error al comprobar {}".format("la excepcion Unauthorized"))
            raise IceGauntlet.Unauthorized(str("la excepcion"))

    def remove(self , token , roomName , current=None):
        '''hola'''
        if True:
            with open("mapas.json") as fichero_mapas:
                datos_usuario=fichero_mapas.read()
            datos_usuario=json.loads(datos_usuario)

            try:
                if datos_usuario[roomName]["room"] == roomName:
                    if datos_usuario[roomName]["current_token"]==token:
                        datos_usuario.pop(roomName)
                        os.remove("icegauntlet/assets/"+roomName+".json")
            except Exception as error:
                print ("sto no {}".format(error))
                raise IceGauntlet.RoomNotExists("fallo")
            else:
                with open("mapas.json","w") as fichero_mapas:
                    json.dump(datos_usuario,fichero_mapas, indent=2, sort_keys=True)
        else:
            print ("Error al comprobar {}".format("la excepcion"))
            raise IceGauntlet.Unauthorized(str("la excepcion"))

    

class DungeonI(IceGauntlet.Dungeon):
    def getRoom(self,current=None):
        print("hola")
        '''Este metodo es para obtener un mapa'''
        try:
            with open("mapas.json") as fichero_mapas:
                datos_usuario=fichero_mapas.read()
            datos_usuario=json.loads(datos_usuario)
        except:
            print("No se ha podido leer el fichero json de busqueda")
        else:
            room_data = (datos_usuario)
            j=0
            q = random.randrange(1,len(datos_usuario))
            for i in  datos_usuario:
                j=+1
                if j==q:
                    ruta=(str(i) + ".json")
                    if os.path.isfile(ruta):
                        break
                    else:
                        print ("Error {}".format( "no existe este fichero"))
                        raise IceGauntlet.RoomNotExists("fallo")

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