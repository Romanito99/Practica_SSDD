import sys
import os
import json
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ServerI(IceGauntlet.Server):
    '''Clase ServerI'''
    def publish(self , token , roomData , current=None):
        ''' hola '''
        fichero={}
        fichero=(roomData)
        print(fichero["room"])
        with open('tutorial.json','w') as f:
            json.dump(fichero, f)
        with open("mapas.json") as f2:
            c=f2.read()
        datos_usuario=json.loads(c)
        datos_usuario[fichero["room"]]={}
        datos_usuario[fichero["room"]]["current_token"]=token
        
        with open('mapas.json', 'w') as contents:
            json.dump(datos_usuario, contents, indent=2, sort_keys=True)
        
        
        

    def getRoom(self,argv):
        '''Este metodo es para obtener un mapa'''
        try :
            try:
                with open("tutorial.json") as f:
                    datos_usuario=f.read()
                datos_usuario=json.loads(datos_usuario)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                room_data = (datos_usuario) 
                self.publish(1,datos_usuario) 
                

                
               
                
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

   
        

    def remove(self , token , roomName , current=None): 
        '''hola'''
        try: 
            os.remove('problema.json')
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

class Server(Ice.Application):
    '''Clase server '''
    def run(self,argv):
        print("estoy echo otro puto")

ServerI().getRoom(sys.argv)