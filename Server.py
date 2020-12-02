import sys
import os
import json
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import ast
import random

class ServerI(IceGauntlet.Server):

    '''Clase ServerI'''
    def __init__(self,authserver):
        self.authserver=authserver 

    def Publish(self , token , roomData , current=None):
        print("hola")
        ''' hola '''
        if (True):
        
            fichero=ast.literal_eval(roomData)
            try:
                data=fichero["data"]
                room=fichero["room"]
                print(room)
            except Exception as error:
                print ("Error {}".format(error))
                raise IceGauntlet.WrongRoomFormat(str(error))
            else:
                if(os.path.isfile("icegauntlet/assets/"+fichero["room"]+".json")):
                    print ("Error {}".format("este fichero ya existe "))
                    raise IceGauntlet.WrongRoomFormat()
                else:
                    with open(("icegauntlet/assets/"+fichero["room"]+".json"),"w") as f:
                        json.dump(fichero, f)

                    with open("mapas.json") as f2:
                        c=f2.read()
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
    
    def Remove(self , token , roomName , current=None): 
        print("hola")
        '''hola'''
        if (True):
            with open("mapas.json") as f:
                datos_usuario=f.read()
            datos_usuario=json.loads(datos_usuario)
            
            try:
                if(datos_usuario[roomName]["room"] == roomName):
                   if((datos_usuario[roomName]["current_token"])==token):
                    t=datos_usuario.pop(roomName)
                    os.remove("icegauntlet/assets/"+roomName+".json")
            except Exception as error:
                print ("sto no {}".format(error))
                raise IceGauntlet.RoomNotExists(str(error))
            else:
                with open("mapas.json","w") as f:
                    json.dump(datos_usuario,f, indent=2, sort_keys=True)
        else:         
            print ("Error al comprobar {}".format("la excepcion"))
            raise IceGauntlet.Unauthorized(str("la excepcion")) 
                          
                            

        
        

    def getRoom():
        '''Este metodo es para obtener un mapa'''
        
        try:
            
            with open("mapas.json") as f:
                datos_usuario=f.read()
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
                    if(os.path.isfile(ruta)):
                        break
                    else:
                        print ("Error {}".format( "no existe este fichero"))
                raise IceGauntlet.RoomNotExists(str(error))


                
        
        
        

   
        

    
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
        print(proxy)
        adapter.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0

Server().main(sys.argv)