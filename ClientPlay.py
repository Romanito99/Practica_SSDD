import sys 
import Ice 
import os
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

class ClientPlay(Ice.Application): 
    def run (self,argv):