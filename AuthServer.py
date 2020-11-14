import sys 
import Ice 
import os
Ice.loadSlice('icegauntlet')
import IceGauntlet
class AuthServerI(icegauntlet.AuthServer): 
    def IsValid(self, token , current=None ): 
        try:

        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))

    def getNewToken (self , user , passHash , current=None):
        try:

        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))
            

    def changePassword (self, user , currentPassHash, current=None):
        try:

        except Exception as error:
            print ("Error al comprobar {}".format(error))
            raise IceGauntlet.Unauthorized(str(error))
            
class AuthServer (Ice.Apllication): 
    def run(): 