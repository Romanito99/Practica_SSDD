import sys
import os
import json
import ast
import random
import glob
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

class Prueba ( ):
    def Prueba(self , argv):
        lista=glob.glob(os.path.join('mapas','*.json'))
        print(len(lista))
Prueba().Prueba(sys.argv)