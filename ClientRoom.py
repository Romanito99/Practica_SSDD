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
'''
    Room Manager Client
'''

import sys
import json
import argparse
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet


class ClientRoom(Ice.Application):
    '''This Class permit us publish or remove a room'''
    def args_parser(self):
        '''This method let us introduce the new password'''
        description = 'Choose Proxy, token, file and option: 1.Publish 2.Remove'
        parser = argparse.ArgumentParser(description)
        parser.add_argument("-p","--proxy",required=True, help='proxy',type=str)
        parser.add_argument("-t","--token",required=True,help='token',type=str)
        parser.add_argument("-f","--file",required=True,help='file json',type=str)
        parser.add_argument("-o","--option",required=True,help='option',type=str)
        args=parser.parse_args()
        return args

    def run(self,args):
        '''This method is our main'''
        args = self.args_parser()
        proxy=args.proxy
        token=args.token
        room_data=str(args.file)
        option=args.option
        broker=self.communicator()
        print(proxy)
        proxy_room_manager = broker.stringToProxy(str(proxy))
        print(proxy_room_manager)
        room_manager=IceGauntlet.RoomManagerPrx.checkedCast(proxy_room_manager)

        if not room_manager:
            raise RuntimeError('Invalid Proxy')

        if option == "1":
            try:
                with open(room_data) as file:
                    user_data=file.read()
                user_data=json.loads(user_data)
            except Exception:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                room_manager.publish(str(token),str(user_data))
        elif option == "2":
            try:
                with open(room_data) as file:
                    user_data=file.read()
                user_data=json.loads(user_data)
            except Exception:
                print("No se ha podido leer el fichero json de busqueda")
            else:
                room_data=user_data["room"]
                room_manager.remove(str(token),str(room_data))

ClientRoom().main(sys.argv)
