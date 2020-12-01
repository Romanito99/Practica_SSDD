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
            n_fichero='fichero.json'
            with open((n_fichero),"w") as f:
                json.dump(fichero, f)

            with open("mapas.json") as f2:
                c=f2.read()
            mapas=json.loads(c)
            
            mapas[n_fichero]={}
            mapas[n_fichero]["current_token"]=token
            mapas[n_fichero]["room"]=fichero["room"]
            print(mapas[n_fichero]["room"])
            
            
            with open('mapas.json', 'w') as contents:
                json.dump(mapas, contents, indent=2, sort_keys=True)
    
    def Remove(self , token , roomName , current=None): 
        '''hola'''
        try: 
            if (self.authserver.isValid(token)):
                with open("mapas.json") as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
                for i in datos_usuario:
                    
                    if(i["room"]== roomName):
                        print("entra aqui",datos_usuario[i]["current_token"])
                        if((i["current_token"])==token):
                            os.remove('juan.json')
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

        
        

    def getRoom():
        '''Este metodo es para obtener un mapa'''
        try :
            try:
                n_fichero = 'mapas.json'
                with open(str(n_fichero)) as f:
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
                        print(i)
                        break
                
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))
        
        

   
        

    
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