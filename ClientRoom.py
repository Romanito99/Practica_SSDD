import sys 
import Ice 
import os
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ClientRoom(Ice.Application): 
    def run (self,argv):

       