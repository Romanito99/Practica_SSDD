import sys
import os
import json
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ServerI(IceGauntlet.Server):
    '''Clase ServerI'''
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
                room_data = (datos_usuario["data"][1])   

        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

    def publish(self , token , roomData , current=None):
        ''' hola '''
        print("toy echo un puto")

    def remove(self , token , roomName , current=None): 
        '''hola'''
        try: 
            print("estoy echo otro puto")
        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

class Server(Ice.Application):
    '''Clase server '''
    def run(self,argv):
        print("estoy echo otro puto")

ServerI().getRoom(sys.argv)