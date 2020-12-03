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
        lista=glob.glob(os.path.join('hola','*.json'))
        q = random.randrange(1,len(lista))
        print(lista.pop(q))

        print(lista)

Prueba().Prueba(sys.argv)