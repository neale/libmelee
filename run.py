#!/usr/bin/python3
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
                        help='Debug mode. Creates a CSV of all game state')
    args = parser.parse_args()
    return args


def signal_handler(signal, frame):
    dolphin.terminate()
    print("Shutting down cleanly...")
    sys.exit(0)

def main():
    
    args = collect_args()
    log = None
    if args.debug:
        log = melee.logger.Logger()
    opponent_type = melee.enums.ControllerType.UNPLUGGED
    if args.live:
        opponent_type = melee.enums.ControllerType.GCN_ADAPTER
    dolphin = melee.dolphin.Dolphin(ai_port=args.port, opponent_port=args.opponent, opponent_type=opponent_type, logger=log)
    gamestate = melee.gamestate.GameState(dolphin)
    controller = melee.controller.Controller(port=args.port, dolphin=dolphin)
    print("Starting Dolphin")
    signal.signal(signal.SIGINT, signal_handler)
    dolphin.run(render=True)
    # Due to how named pipes work, this has to come AFTER running dolphin
    controller.connect()
    print("Connected controller to emulator")


    #Main loop
    while True:
        #"step" to the next frame
        gamestate.step()
        #What menu are we in?
        if gamestate.menu_state == melee.enums.Menu.IN_GAME:
            #XXX: This is where your AI does all of its stuff!
            #This line will get hit once per frame, so here is where you read
            #   in the gamestate and decide what buttons to push on the controller
            #melee.techskill.multishine(ai_state=gamestate.ai_state, controller=controller)
            r = len(melee.techskill.manager['actions'])
            action = melee.techskill.manager['actions'][np.random.randint(0, r)]
            print(action)
            action(ai_state=gamestate.ai_state, controller=controller)
        #If we're at the character select screen, choose our character
        elif gamestate.menu_state == melee.enums.Menu.CHARACTER_SELECT:
            melee.menuhelper.choosecharacter(character=melee.enums.Character.FOX,
                gamestate=gamestate, controller=controller, swag=True,
                start=True)
        #If we're at the postgame scores screen, spam START
        elif gamestate.menu_state == melee.enums.Menu.POSTGAME_SCORES:
            melee.menuhelper.skippostgame(controller=controller)
        #If we're at the stage select screen, choose a stage
        elif gamestate.menu_state == melee.enums.Menu.STAGE_SELECT:
            melee.menuhelper.choosestage(stage=melee.enums.Stage.POKEMON_STADIUM,
                gamestate=gamestate, controller=controller)
        #Flush any button presses queued up
        controller.flush()
        if log:
            log.logframe(gamestate)
            log.writeframe()

if __name__ == "__main__":
    main()
