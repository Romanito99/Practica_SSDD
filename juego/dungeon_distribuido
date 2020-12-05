#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W1203

'''
    ICE Gauntlet LOCAL GAME
'''

import sys
import atexit
import logging
import argparse
import Ice
import ast
Ice.loadSlice('icegauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

import json
import game
import game.common
import game.screens
import game.pyxeltools
import game.orchestration




EXIT_OK = 0
BAD_COMMAND_LINE = 1

DEFAULT_ROOM = 'tutorial.json'
DEFAULT_HERO = game.common.HEROES[0]


@atexit.register
# pylint: disable=W0613
class DungeonMapDistribuido():
    '''Store a list of rooms'''
    def __init__(self ):
        communicator = Ice.initialize(sys.argv)
        dungeon_proxy=communicator.stringToProxy(sys.argv[1])
        self.dungeon=IceGauntlet.DungeonPrx.checkedCast(dungeon_proxy)

    @property
    def next_room(self):
        #este esta por hacer
        fichero = self.dungeon.getRoom()
        fichero=ast.literal_eval(fichero)
        with open(("tutorial.json"),"w") as fichero_mapas:
            json.dump(fichero, fichero_mapas)
            
        return 'tutorial.json'
            

    @property
    def finished(self):
        return False
def bye(*args, **kwargs):
    '''Exit callback, use for shoutdown'''
    print('Thanks for playing!')
# pylint: enable=W0613

def parse_commandline():
    '''Parse and check commandline'''
    parser = argparse.ArgumentParser('IceDungeon Local Game')
    parser.add_argument('PROXY', nargs='+', default=[DEFAULT_ROOM], help='List of levels')
    parser.add_argument(
        '-p', '--player', default=DEFAULT_HERO, choices=game.common.HEROES,
        dest='hero', help='Hero to play with'
    )
    options = parser.parse_args()

    '''for level_file in options.PROXY:
        if not game.assets.search(level_file):
            logging.error(f'Level "{level_file}" not found!')
            return None'''
    return options  




def main():
    '''Start game according to commandline'''
    user_options = parse_commandline()
    if not user_options:
        return BAD_COMMAND_LINE

    dungeon = DungeonMapDistribuido()
    game.pyxeltools.initialize()
    gauntlet = game.Game(user_options.hero, dungeon)
    gauntlet.add_state(game.screens.TileScreen, game.common.INITIAL_SCREEN)
    gauntlet.add_state(game.screens.StatsScreen, game.common.STATUS_SCREEN)
    gauntlet.add_state(game.screens.GameScreen, game.common.GAME_SCREEN)
    gauntlet.add_state(game.screens.GameOverScreen, game.common.GAME_OVER_SCREEN)
    gauntlet.add_state(game.screens.GoodEndScreen, game.common.GOOD_END_SCREEN)
    gauntlet.start()

    return EXIT_OK


if __name__ == '__main__':
    sys.exit(main())
