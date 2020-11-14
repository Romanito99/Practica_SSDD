import sys 
import Ice 
import os
Ice.loadSlice('icegauntlet')
import IceGauntlet

class ServerI(icegauntlet.AuthServer):
    def getRoom():
        try :

        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))
    def Publish(self , token , roomData , current=None):
     
    
    def Remove(self , token , roomName , current=None): 
        try: 

        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

class Server(Ice.Apllication): 
    def run(): 