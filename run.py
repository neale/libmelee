#!/usr/bin/python3
import datetime
import collections
import melee
import argparse
import signal
import numpy as np
import sys

#This example program demonstrates how to use the Melee API to run dolphin programatically,
#   setup controllers, and send button presses over to dolphin

def check_port(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 4:
         raise argparse.ArgumentTypeError("%s is an invalid controller port. \
         Must be 1, 2, 3, or 4." % value)
    return ivalue

def collect_args():
    chain = None
    parser = argparse.ArgumentParser(description='Example of libmelee in action')
    parser.add_argument('--port', '-p', type=check_port,
                        help='The controller port your AI will play on',
                        default=2)
    parser.add_argument('--opponent', '-o', type=check_port,
                        help='The controller port the opponent will play on',
                        default=1)
    parser.add_argument('--live', '-l',
                        help='The opponent playing live with a GCN Adapter',
                        default=True)
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Debug mode. Creates a CSV of all game state', 
                        default=True)
    parser.add_argument('--train', '-t', action='store_false',
                        help='train the deep neural network',
                        default=False)
    args = parser.parse_args()
    return args


def signal_handler(signal, frame):
    dolphin.terminate()
    print("Shutting down cleanly...")
    sys.exit(0)

def get_time():
    return str(datetime.datetime.now())[11:].split(".")[0]

def main():
    
    args = collect_args()
    log = None
    if args.debug:
        #log = melee.logger.Logger()
        actionlog = melee.logger.ActionLogger()
    opponent_type = melee.enums.ControllerType.UNPLUGGED
    if args.live:
        opponent_type = melee.enums.ControllerType.STANDARD
    dolphin = melee.dolphin.Dolphin(ai_port=args.port, opponent_port=args.opponent, opponent_type=opponent_type, logger=log)
    gamestate = melee.gamestate.GameState(dolphin)
    controller = melee.controller.Controller(port=args.port, dolphin=dolphin)
    print("Starting Dolphin")
    signal.signal(signal.SIGINT, signal_handler)
    dolphin.run(render=True)
    # Due to how named pipes work, this has to come AFTER running dolphin
    controller.connect()
    print("Connected controller to emulator")
    print("STARTING: {}".format(get_time()))
    #Main loop
    state = 0
    current_state = "START"
    r = len(melee.techskill.manager['actions'])
    while True:
        #"step" to the next frame
        gamestate.step()
        
        if gamestate.menu_state == melee.enums.Menu.IN_GAME:
            if (state == 1) :
                action = melee.techskill.manager['actions'][np.random.randint(0, r)]
                print ("{} GAMESTATE: IN_GAME, ACTION: {}".format(get_time(), action.__name__))
                action(ai_state=gamestate.ai_state, controller=controller)
                if log:
                    actionlog.actionlogger(gamestate, action.__name__)
                    actionlog.writeframe()
                    actionlog.writelog()
                state = 0;
            else:
                state += 1
        #If we're at the character select screen, choose our character
        elif gamestate.menu_state == melee.enums.Menu.CHARACTER_SELECT:
            if current_state is not "CHARACTER_SELECT":
                print("{} GAMESTATE: CHARACTER SELECT".format(get_time()))
                current_state = "CHARACTER_SELECT"

            melee.menuhelper.choosecharacter(character=melee.enums.Character.FOX,
                gamestate=gamestate, controller=controller, swag=True,
                start=False)
        #If we're at the postgame scores screen, spam START
        elif gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
            if current_state is not "POSTGAME_SCORES":
                print ("{} GAMESTATE: POSTGAME_SCORES".format(get_time()))
                current_state = "POSTGAME_SCORES"

            melee.menuhelper.skippostgame(controller=controller)
        #If we're at the stage select screen, choose a stage
        elif gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
            if current_state is not "STAGE_SELECT":
                print ("{} GAMESTATE: STATE_SELECT".format(get_time()))
                current_state = "STAGE_SELECT"
            if args.train:    
                melee.menuhelper.choosestage(stage=melee.enums.Stage.FINAL_DESTINATION,
                    gamestate=gamestate, controller=controller)
            else: pass
        #Flush any button presses queued up
        controller.flush()

if __name__ == "__main__":
    main()
