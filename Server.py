import sys
import os
import json
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import ast

class ServerI(IceGauntlet.Server):
    '''Clase ServerI'''
    def publish(self , token , roomData , current=None):
        ''' hola '''
        if (isValid(token)):
        
            fichero=ast.literal_eval(roomData)
            with open('juan.json','w') as f:
                json.dump(fichero, f)

            with open("mapas.json") as f2:
                c=f2.read()
            mapas=json.loads(c)
            mapas[fichero["room"]]={}
            mapas[fichero["room"]]["current_token"]=token
            
            with open('mapas.json', 'w') as contents:
                json.dump(mapas, contents, indent=2, sort_keys=True)
    
    def remove(self , token , roomName , current=None): 
        '''hola'''
        try: 
            if (True):
                with open("mapas.json") as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
                for i in datos_usuario:
                    
                    if(datos_usuario== roomName):
                        print("entra aqui")
                        if(int(atos_usuario["current_token"])==token):
                            os.remove('juan.json')
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

        
        

    def getRoom(self,argv):
        '''Este metodo es para obtener un mapa'''
        try :
            try:
                with open("juego/assets/level_2.json") as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                room_data = (datos_usuario) 
                
                #self.publish(2,str(datos_usuario) )
                self.remove(2,str(datos_usuario["room"]))
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

   
        

    
class Server(Ice.Application):
    '''Clase server '''
    def run(self,argv):
        print("estoy echo otro puto")

ServerI().getRoom(sys.argv)