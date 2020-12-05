import sys
import os
import json
import ast
import random
import glob
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class RoomManagerI(IceGauntlet.RoomManager):

    '''Clase ServerI'''
    def __init__(self,authserver):
        self.authserver=authserver

    def publish(self , token , room_data , current=None):
        repetido=False

        if self.authserver.isValid(token):
            fichero=ast.literal_eval(room_data)
            try:
                
                data=fichero["data"]
                room=fichero["room"]
                
            except Exception as error:
                print ("Error {}".format(error))
                raise IceGauntlet.WrongRoomFormat(str(error))
            else:
                
                lista=glob.glob(os.path.join('maps','*.json'))
                
                for i in lista:
                    
                    with open(str(i))as fichero_mapas:
                        datos_mapa=fichero_mapas.read()
                    datos_mapa=json.loads(datos_mapa)
                    
                    if datos_mapa["data"] == fichero["data"] and datos_mapa["current_token"]!=str(token):
                        print ("Error: {}".format("Room Already Exists Exception"))
                        raise IceGauntlet.RoomAlreadyExists("File already exists")
                    elif datos_mapa["data"] == fichero["data"] and datos_mapa["current_token"]==str(token):
                        print("This map exists or it's not yours")
                        repetido=True
                        break
                if not repetido:  
                    i=len(lista)+random.randrange(1,1000000)

                    nombre="maps/level"+str(i)+".json"    
                    with open((nombre),"w") as fichero_mapas:
                        json.dump(fichero, fichero_mapas)

                    with open(nombre) as fichero_mapas2:
                        c=fichero_mapas2.read()
                    mapas=json.loads(c)
                    mapas["current_token"]=token
                    with open((nombre),"w") as fichero_mapas3:
                        json.dump(mapas, fichero_mapas3)

            
        else:
            print ("Error: {}".format("Unauthorized Exception"))
            raise IceGauntlet.Unauthorized()

    def remove(self , token , roomName , current=None):
        borrado=False
        '''hola'''
        if self.authserver.isValid(token):
            
            lista=glob.glob(os.path.join('maps','*.json'))
            for i in lista:
                mapa=str(i)
                
                with open(mapa) as fichero_mapas:
                    datos_mapa=fichero_mapas.read()
                datos_mapa=json.loads(datos_mapa)
                print(datos_mapa["room"], roomName)
                if  datos_mapa["room"] == str(roomName) and str(token)==datos_mapa["current_token"]:
                    os.remove(mapa)
                    borrado=True
                    break
                
            if not borrado:            
                raise IceGauntlet.RoomNotExists("Este mapa no existe o no es tuyo")
                    
        else:
            print ("Error al comprobar {}".format("la excepcion"))
            raise IceGauntlet.Unauthorized(str("la excepcion"))

    

class DungeonI(IceGauntlet.Dungeon):
    def getRoom(self,current=None):
        '''Este metodo es para obtener un mapa'''                     
        
        try: 
            lista=glob.glob(os.path.join('maps','*.json'))
            q = random.randrange(0,len(lista))
            ruta=(lista.pop(q))
            with open(str(ruta)) as fichero_mapas:
                datos_usuario=fichero_mapas.read()
            datos_usuario=json.loads(datos_usuario)
            datos_usuario.pop("current_token")
            print(datos_usuario)
        except Exception as error:
            raise IceGauntlet.RoomNotExists("El servidor no tiene ningun mapa") 
        return str(datos_usuario)

    
class RoomManager(Ice.Application):
    '''Clase server '''
    def run(self, argv):
        proxy=self.communicator().stringToProxy(argv[1])
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy)
        print(proxy)
        if not authserver:
            raise RunTimeError('Invalid Proxy')
        servant=RoomManagerI(authserver)
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('RoomManager'))
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

RoomManager().main(sys.argv)