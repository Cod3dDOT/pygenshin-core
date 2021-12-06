from pynput.mouse import Button
from pynput.keyboard import Key

class MOUSEBUTTONS:
    LEFT    = Button.left
    RIGHT   = Button.right


class KEY:
    #from https://pynput.readthedocs.io/en/latest/keyboard.html
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'

    N0 = '0'
    N1 = '1'
    N2 = '2'
    N3 = '3'
    N4 = '4'
    N5 = '5'
    N6 = '6'
    N7 = '7'
    N8 = '8'
    N9 = '9'

    ENTER       = Key.enter
    ESCAPE      = Key.esc
    BACKSPACE   = Key.backspace
    CAPS        = Key.caps_lock
    DELETE      = Key.delete

    SHIFT       = Key.shift
    SHIFT_LEFT  = Key.shift_l
    SHIFT_RIGHT = Key.shift_r

    CTRL       = Key.ctrl 
    CTRL_LEFT  = Key.ctrl_l
    CTRL_RIGHT = Key.ctrl_r

    ALT         = Key.alt
    ALT_LEFT    = Key.alt_l
    ALT_RIGHT   = Key.alt_r

    ARROW_UP    = Key.up
    ARROW_DOWN  = Key.down
    ARROW_RIGHT = Key.right
    ARROW_LEFT  = Key.left

class KEYBINDINGS:
    MOVE_FORWARD    = KEY.W
    MOVE_BACKWARD   = KEY.S
    MOVE_RIGHT      = KEY.D
    MOVE_LEFT       = KEY.A

    SWITCH_WALK_RUN = KEY.CTRL_LEFT

    NORMAL_ATTACK   = MOUSEBUTTONS.LEFT