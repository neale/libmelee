"""Helper functions for with some techskill examples"""

from melee import enums

"""Higher order funtions for character actions"""

"""Frame-perfect Multishines as Fox"""
def multishine(ai_state, controller, tilt=(.5, .5)):
    #If standing, shine
    if ai_state.action == enums.Action.STANDING:
        controller.press_button(enums.Button.BUTTON_B)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
        return

    #Shine on frame 3 of knee bend, else nothing
    if ai_state.action == enums.Action.KNEE_BEND:
        if ai_state.action_frame == 2:
            controller.press_button(enums.Button.BUTTON_B)
            controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
            return
        else:
            controller.empty_input()
            return

    isInShineStart = (ai_state.action == enums.Action.DOWN_B_STUN or
            ai_state.action == enums.Action.DOWN_B_GROUND_START)

    #Jump out of shine
    if isInShineStart and ai_state.action_frame >= 4 and ai_state.on_ground:
        controller.press_button(enums.Button.BUTTON_Y)
        return

    if ai_state.action == enums.Action.DOWN_B_GROUND:
        controller.press_button(enums.Button.BUTTON_Y)
        return

    controller.empty_input()

def jump_forward(ai_state, controller, tilt=(.5, .5)):
    # Continually jump forever, fun?
    if ai_state.action == enums.Action.STANDING:
        controller.press_button(enums.Button.BUTTON_Y)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, tilt[0], tilt[1])
        return

    isJumping = (ai_state.action == enums.Action.JUMPING_FORWARD or
        ai_state.action == enums.Action.JUMPING_BACKWARD)

    if isJumping and ai_state.action_frame >= 2 and not ai_state.on_ground:
        controller.press_button(enums.Button.BUTTON_Y)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, tilt[0], tilt[1])
        return
        
    controller.empty_input()

#def jump_backward(ai_state, controller):
def run_forward(ai_state, controller, tilt=(.5, .5)):
    #pretty much run forward no matter what, may refine later
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, .5)
    return

def run_backward(ai_state, controller, tilt=(.5, .5)):
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
    return 

def smash_up_up(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 1)
    return

def smash_up_down(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
    return

def smash_up_left(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
    return

def smash_up_right(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 1)
    return

def smash_down(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
    return

def smash_left(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
    return

def smash_right(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_B)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, .5)
    return

def attack_up(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_A)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 1)
    return

def attack_down(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_A)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
    return

def attack_left(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_A)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
    return

def attack_right(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_A)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, .5)
    return

def shield(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_L)
    return

def roll_right(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_L)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
    return

def roll_left(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_L)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, .5)
    return

def grab(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_Z)
    return

def test(ai_state, controller, tilt=(.5, .5)):
    controller.press_button(enums.Button.BUTTON_A)
    controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
    return

def get_actions():
    return manager

manager = {"actions" : [
                        run_forward, run_backward, smash_up_up, smash_up_down, 
                        smash_up_right, smash_up_left, smash_down, smash_right, 
                        smash_left, attack_up, attack_down, attack_left, 
                        attack_right, shield, roll_right, roll_left, grab, 
                        jump_forward, test
                       ]
          }


