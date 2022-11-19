# Simulates actual physical action of pressing a keyboard key as opposed to programmatically
# simulating a keypress. TIP: For cleaner code, save as separate file and import it.

import ctypes
from ctypes import wintypes
import time

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)   # Alt
    PressKey(VK_TAB)    # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU) # Alt~

special_char_dict={'`':0xC0, '~':[0xC0], '1':0x31, '!':[0x31], \
 '2':0x32, '@':[0x32], '3':0x33, '#':[0x33], '4':0x34, '$':[0x34],\
 '5':0x35, '%':[0x35], '6':0x36, '^':[0x36], '7':0x37, '&':[0x37],\
 '8':0x38, '*':[0x38], '9':0x39, '(':[0x39], '0':0x30, ')':[0x30],\
 '-':0xBD, '_':[0xBD], '+':0xBB, '=':[0xBB], ';':0xBA, ':':[0xBA],\
 "'":0xDE, '"':[0xDE], '\\':0xE2, '|':[0xE2], ']':0xDD, '}':[0xDD],\
 '[':0xDB, '{':[0xDB], ',':0xBC, '<':[0xBC], '.':0xBE, '>':[0xBE],\
 '/':0xBF, '?':[0xBF], 'a':0x41, 'A':[0x41], 'b':0x42, 'B':[0x42],\
 'c':0x43, 'C':[0x43], 'd':0x44, 'D':[0x44], 'e':0x45, 'E':[0x45],\
 'f':0x46, 'F':[0x46], 'g':0x47, 'G':[0x47], 'h':0x48, 'H':[0x48],\
 'i':0x49, 'I':[0x49], 'j':0x4A, 'J':[0x4A], 'k':0x4B, 'K':[0x4B],\
 'l':0x4C, 'L':[0x4C], 'm':0x4D, 'M':[0x4D], 'n':0x4E, 'N':[0x4E],\
 'o':0x4F, 'O':[0x4F], 'p':0x50, 'P':[0x50], 'q':0x51, 'Q':[0x51],\
 'r':0x52, 'R':[0x52], 's':0x53, 'S':[0x53], 't':0x54, 'T':[0x54],\
 'u':0x55, 'U':[0x55], 'v':0x56, 'V':[0x56], 'w':0x57, 'W':[0x57],\
 'x':0x58, 'X':[0x58], 'y':0x59, 'Y':[0x59], 'z':0x5A, 'Z':[0x5A],\
 ' ':0x20, '\n':0x20}


def keyboard_simulation(string):
    time.sleep(5)

    for letter in string:
        keys= letter
        character= special_char_dict.get(keys,0x20)
        if type(character) is list:
            PressKey(0x10)
            PressKey(character[0])
            ReleaseKey(character[0])
            ReleaseKey(0x10)
        else:
            PressKey(character)
            ReleaseKey(character)


