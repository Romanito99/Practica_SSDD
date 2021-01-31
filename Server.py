#!/usr/bin/env python3
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
   Server
'''

import sys
import os
import json
import ast
import random
import uuid
import glob
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import IceStorm

lista={}
listamapas={}

class RoomManagerI(IceGauntlet.RoomManager):
    '''This Class publish or remove a map'''

    def __init__(self , authserver , id , room_manager_sync_channel_prx):
        '''This method is our init'''
        self.authserver=authserver
        self.room_manager_sync_channel_prx=room_manager_sync_channel_prx
        self.id=id

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
                server_sync_prx = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(self.room_manager_sync_channel_prx.getPublisher())
                server_sync_prx.newRoom(room_data["room"], self.id)

    def remove(self , token , roomName , current=None):
        '''This method remove a room from an authorized user'''
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
        server_sync_prx = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(self.room_manager_sync_channel_prx.getPublisher())
        server_sync_prx.removedRoom(roomName)

    def getRoom(self,room,current=None):
        '''This method read the room from our directory'''
        map_list=glob.glob(os.path.join('maps','*.json'))
        for i in map_list:
            with open(str(i))as maps_file:
                data_map=maps_file.read()
            data_map=json.loads(data_map)
            if data_map["room"] == room:
                return str(data_map)


class DungeonI(IceGauntlet.Dungeon):
    '''Class for DungeonI'''
    def getRoom(self,current=None):
        '''This method obtain the map'''
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

class RoomManagerSyncI(IceGauntlet.RoomManagerSync):
    '''Class for the events from the RoomManagerSync'''

    def hello(self, room_manager_prx, id_server, current=None):
        '''This method is for the event Hello which connect one server with the server pool'''
        print(' HELLO ' +self.server.id+ ' conoce al nuevo servidor  ' + id_server)
        lista[id_server]= room_manager_prx
        listamapas[self.server.id]={}
        if self.server.id != id_server:
            self.server.server_sync_prx.announce(self.server.room_manager_prx, self.server.id)

    def announce(self, room_manager_prx, id_server, current=None):
        '''This method is for the event Announce which response a Hello event'''
        lista_id=lista.keys()

        if self.server.id != id_server and id_server not in lista_id:
            print('ANNOUNCE '+id_server+' se presenta ' + self.server.id)
            lista[id_server]= room_manager_prx

    def newRoom(self, roomName, id_server, current=None):
        '''This method is for the event newRoom which notify that a new map is received'''
        print('"NEW ROOM" El servidor ' +id_server+ ' ha obtenido el mapa ' +roomName)
        newRoom=lista[id_server].getRoom(roomName)

    def removedRoom(self,roomName, current=None):
        '''This method is for the event newRoom which notify that a map is removed'''
        print('"REMOVED ROOM" Se  ha eliminado el mapa: '+ roomName)

class RoomManager(Ice.Application):
    '''Clase server '''
    room_manager_prx=None
    id=None
    room_manager_sync_channel_prx=None
    server_sync_prx=None

    def run(self, args):

        proxy = self.communicator().propertyToProxy("property_authorization")
        authserver=IceGauntlet.AuthenticationPrx.checkedCast(proxy)
        if not authserver:
            raise RunTimeError('Invalid Proxy')

        self.id = uuid.uuid4().hex
        adapter = self.communicator().createObjectAdapter('ServerAdapter')
        servant=RoomManagerI(authserver,None,None)
        proxy = adapter.add(servant,Ice.stringToIdentity("maps_" +self.id))
        print('"{}"'.format(proxy), flush=True)
        icestorm_proxy = self.communicator().stringToProxy("SSDD-CONEJO-BRAOJOS.IceStorm/TopicManager")

        if icestorm_proxy is None:
            print("property '{}' not set".format("SSDD-Braojos.IceStorm/TopicManager"))
            return None

        icestorm_topic_manager = IceStorm.TopicManagerPrx.uncheckedCast(icestorm_proxy)
        if not icestorm_topic_manager:
            print("Invalid topic manager")
            return 1

        try:
            self.room_manager_sync_channel_prx = icestorm_topic_manager.retrieve("RoomManagerSyncChannel")
        except IceStorm.NoSuchTopic:
            self.room_manager_sync_channel_prx = icestorm_topic_manager.create("RoomManagerSyncChannel")

        self.room_manager_prx = IceGauntlet.RoomManagerPrx.uncheckedCast(proxy)
        servant.room_manager_sync_channel_prx=self.room_manager_sync_channel_prx
        servant.id=self.id
        eventos=RoomManagerSyncI()
        eventos.server=self
        self.server_sync_prx = adapter.addWithUUID(eventos)
        self.room_manager_sync_channel_prx.subscribeAndGetPublisher(dict(),self.server_sync_prx)
        adapter.activate()
        self.server_sync_prx = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(self.room_manager_sync_channel_prx.getPublisher())
        listamapas[self.id]={}
        self.server_sync_prx.hello(self.room_manager_prx, self.id)
        servant_juego=DungeonI()
        adapter_dungeon = self.communicator().createObjectAdapter('DungeonAdapter')
        proxy_dungeon = adapter.add(servant_juego, Ice.stringToIdentity("proxy_dungeon_"+self.id))
        adapter_dungeon.activate()
        self.communicator().waitForShutdown()

        return 0

if __name__ == '__main__':
    app = RoomManager()
    sys.exit(app.main(sys.argv))
