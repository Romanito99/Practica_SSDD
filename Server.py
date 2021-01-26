# Quitamos estos errores debido a que el import IceGauntlet no se puede determinar antes
# pylint: disable=E0401
# pylint: disable=C0413
# Quitamos este error ya que la linea 6 es una justificacion y no importa que sea tan larga
# pylint: disable=C0301
# Quitamos este error debido a que, segun lo aprendido, no es una mala forma de llamar a nuestra clase
# pylint: disable=C0103
# Quitamos este error debido a que RunTimeError es una excepcion
# pylint: disable=E0602
# Quitamos este error debido a que 'current' es necesario pasarlo como arg
# pylint: disable=W0613
'''
    Room Manager Server and Game Server
'''

import sys
import os
import json
import ast
import random
import glob
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class RoomManagerI(IceGauntlet.RoomManager):
    '''This Class publish or remove a map'''
    def __init__(self,authserver):
        '''This method is our init'''
        self.authserver=authserver

    def publish(self , token , room_data , current=None):
        '''This metod publish a new map if it doesn't exists'''
        file_exists=False
        user = self.authserver.getOwner(token)
        room_data=ast.literal_eval(room_data)
        try:
            data=room_data["data"]
            room_data["room"]
        except Exception:
            print ("Error: {}".format("WrongRoomFormat Exception"))
            raise IceGauntlet.WrongRoomFormat()

        else:
            map_list=glob.glob(os.path.join('maps','*.json'))

            for i in map_list:
                with open(str(i))as maps_file:
                    data_map=maps_file.read()
                data_map=json.loads(data_map)

                if data_map["data"] == data:

                    if data_map["user"]!=str(user):
                        print ("Error: {}".format("Room Already Exists Exception"))
                        raise IceGauntlet.RoomAlreadyExists()
                    else:
                        file_exists=True
                        break

            if not file_exists:
                i=len(map_list)+random.randrange(1,1000000)
                map_name="maps/level"+str(i)+".json"
                with open((map_name),"w") as maps_file:
                    json.dump(room_data, maps_file)

                with open(map_name) as maps_file2:
                    data_map=maps_file2.read()
                maps=json.loads(data_map)
                maps["user"]=user
                with open((map_name),"w") as maps_file3:
                    json.dump(maps, maps_file3)


    def remove(self , token , roomName , current=None):
        '''This metod remove a room from an authorized user'''
        room_found=False
        user = self.authserver.getOwner(token)

        map_list=glob.glob(os.path.join('maps','*.json'))
        for i in map_list:
            map=str(i)
            with open(map) as maps_file:
                data_map=maps_file.read()
            data_map=json.loads(data_map)

            if (data_map["room"]==str(roomName) and str(user)==data_map["user"]):
                os.remove(map)
                room_found=True
                break
        if not room_found:
            print ("Error: {}".format("Room Not Exists Exception "))
            raise IceGauntlet.RoomNotExists()


class DungeonI(IceGauntlet.Dungeon):
    '''Class for DungeonI'''
    def getRoom(self,current=None):
        '''This metod obtain the map'''
        try:
            map_list=glob.glob(os.path.join('maps','*.json'))
            random_map = random.randrange(0,len(map_list))
            path=(map_list.pop(random_map))
            with open(str(path)) as maps_file:
                user_data=maps_file.read()
            user_data=json.loads(user_data)
            user_data.pop("user")
        except Exception:
            print ("Error: {}".format("Room Not Exists Exception"))
            raise IceGauntlet.RoomNotExists()
        return str(user_data)

class RoomManager(Ice.Application):
    '''Clase server '''
    def run(self, argv):
        '''This method is our main'''
        broker=self.communicator()
        proxy=argv[1]
        print(proxy)
        proxy_authserver=broker.stringToProxy(proxy)
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy_authserver)

        if not authserver:
            print ("Error: {}".format("Run Time Error Exception"))
            raise RunTimeError()
        servant=RoomManagerI(authserver)
        adapter = self.communicator().createObjectAdapter('RoomManagerAdapter')
        proxy = adapter.add(servant, self.communicator().stringToIdentity('RoomManager'))
        print('"{}"'.format(proxy), flush=True)
        adapter.activate()
        game_servant=DungeonI()
        adapter_dungeon = self.communicator().createObjectAdapter('DungeonAdapter')
        proxy_dungeon = adapter.add(game_servant, self.communicator().stringToIdentity('dungeon'))
        proxy_dungeon='"'+str(proxy_dungeon)+'"'
        handler = open('dungeon_proxy', 'w')
        handler.write(str(proxy_dungeon))
        handler.close()
        adapter_dungeon.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

RoomManager().main(sys.argv)
