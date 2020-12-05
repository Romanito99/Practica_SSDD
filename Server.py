# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
import sys
import os
import json
import ast
import random
import glob
import Ice
Ice.loadSlice('icegauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet


class RoomManagerI(IceGauntlet.RoomManager):
    '''This Class '''
    def __init__(self,authserver):
        self.authserver=authserver

    def publish(self , token , room_data , current=None):
        '''This metod publish a new map if it doesn't exists'''
        file_exists=False

        if self.authserver.isValid(token):
            room_data=ast.literal_eval(room_data)
            try:
                data=room_data["data"]
                room=room_data["room"]
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

                        if data_map["current_token"]!=str(token):
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
                    maps["current_token"]=token
                    with open((map_name),"w") as maps_file3:
                        json.dump(maps, maps_file3)

        else:
            print ("Error: {}".format("Unauthorized Exception"))
            raise IceGauntlet.Unauthorized()

    def remove(self , token , roomName , current=None):
        '''This metod remove a room from an authorized user'''
        room_found=False
        
        if self.authserver.isValid(token):

            map_list=glob.glob(os.path.join('maps','*.json'))
            for i in map_list:
                map=str(i)
                with open(map) as maps_file:
                    data_map=maps_file.read()
                data_map=json.loads(data_map)

                if (data_map["room"]==str(roomName) and str(token)==data_map["current_token"]):
                    '''Remove the room if it exists and the token is the correct one'''
                    os.remove(map)
                    room_found=True
                    break
            if not room_found:
                '''If the room is not found we have made this exception'''
                print ("Error: {}".format("Room Not Exists Exception "))
                raise IceGauntlet.RoomNotExists()
        else:
            print ("Error: {}".format("Unauthorized Exception"))
            raise IceGauntlet.Unauthorized()

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
            user_data.pop("current_token")
            print(user_data)
        except Exception:
            print ("Error: {}".format("Room Not Exists Exception"))
            raise IceGauntlet.RoomNotExists()
        return str(user_data)

class RoomManager(Ice.Application):
    '''Clase server '''
    def run(self, argv):
        proxy=self.communicator().stringToProxy(argv[1])
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy)

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
        print('"{}"'.format(proxy_dungeon), flush=True)
        adapter_dungeon.activate()
        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()
        return 0

RoomManager().main(sys.argv)