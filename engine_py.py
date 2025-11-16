import ctypes
import os
from ctypes import c_int, c_char, c_char_p, Structure

# Load the DLL
_libname = os.path.join(os.getcwd(), 'game.dll')
_lib = ctypes.CDLL(_libname)

class Card(Structure):
    _fields_ = [('color', ctypes.c_char * 10), ('value', ctypes.c_int)]

# Bind functions
_lib.engine_init.argtypes = []
_lib.engine_init.restype = None

_lib.engine_get_current_player.argtypes = []
_lib.engine_get_current_player.restype = c_int

_lib.engine_get_top_discard.argtypes = []
_lib.engine_get_top_discard.restype = Card

_lib.engine_get_hand_size.argtypes = [c_int]
_lib.engine_get_hand_size.restype = c_int

_lib.engine_get_hand.argtypes = [c_int, ctypes.POINTER(Card), c_int]
_lib.engine_get_hand.restype = c_int

_lib.engine_play_card.argtypes = [c_int, c_int]
_lib.engine_play_card.restype = c_int

_lib.engine_draw_card.argtypes = [c_int]
_lib.engine_draw_card.restype = c_int

_lib.engine_ai_move.argtypes = []
_lib.engine_ai_move.restype = c_int

_lib.engine_next_turn.argtypes = []
_lib.engine_next_turn.restype = None

_lib.engine_check_winner.argtypes = []
_lib.engine_check_winner.restype = c_int


def init():
    _lib.engine_init()


def get_current_player():
    return _lib.engine_get_current_player()


def get_top_discard():
    c = _lib.engine_get_top_discard()
    return (c.color.decode('utf-8').strip('\x00'), c.value)


def get_hand(player):
    size = _lib.engine_get_hand_size(player)
    arr_type = Card * max(1, size)
    arr = arr_type()
    got = _lib.engine_get_hand(player, arr, size)
    res = []
    for i in range(got):
        res.append((arr[i].color.decode('utf-8').strip('\x00'), arr[i].value))
    return res


def play_card(player, position):
    return bool(_lib.engine_play_card(player, position))


def draw_card(player):
    # returns 0 empty, 1 drawn-kept, 2 drawn-played
    return _lib.engine_draw_card(player)


def ai_move():
    return bool(_lib.engine_ai_move())


def next_turn():
    _lib.engine_next_turn()


def check_winner():
    return _lib.engine_check_winner()
