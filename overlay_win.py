# overlay_win.py
# pyright: reportUnreachable=false
"""Windows overlay module for pygame dashboard windows.

Provides functions to configure a pygame window as a borderless,
transparent, click-through overlay that stays on top of other windows.

Only functional on Windows (win32).  On other platforms, all functions
are no-ops.
"""

import ctypes
import sys
from ctypes import wintypes

import pygame

# ----------------------------------------------------------------------
# Win32 API constants
# ----------------------------------------------------------------------
GWL_STYLE = -16
GWL_EXSTYLE = -20

WS_POPUP = 0x80000000
WS_VISIBLE = 0x10000000

WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020

LWA_COLORKEY = 0x00000001
LWA_ALPHA = 0x00000002

HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_SHOWWINDOW = 0x0040
SWP_FRAMECHANGED = 0x0020

SM_CXSCREEN = 0
SM_CYSCREEN = 1


# ----------------------------------------------------------------------
# Win32 API function prototypes — only available on Windows
# ----------------------------------------------------------------------
if sys.platform == "win32":
    user32 = ctypes.windll.user32

    GetForegroundWindow = user32.GetForegroundWindow
    GetForegroundWindow.restype = wintypes.HWND

    SetWindowLongW = user32.SetWindowLongW
    SetWindowLongW.argtypes = (wintypes.HWND, ctypes.c_int, wintypes.LONG)

    GetWindowLongW = user32.GetWindowLongW
    GetWindowLongW.argtypes = (wintypes.HWND, ctypes.c_int)
    GetWindowLongW.restype = wintypes.LONG

    SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
    SetLayeredWindowAttributes.argtypes = (
        wintypes.HWND,
        wintypes.COLORREF,
        wintypes.BYTE,
        wintypes.DWORD,
    )
    SetLayeredWindowAttributes.restype = wintypes.BOOL

    SetWindowPos = user32.SetWindowPos
    SetWindowPos.argtypes = (
        wintypes.HWND,
        wintypes.HWND,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        wintypes.UINT,
    )
    SetWindowPos.restype = wintypes.BOOL

    GetSystemMetrics = user32.GetSystemMetrics
    GetSystemMetrics.argtypes = (ctypes.c_int,)
    GetSystemMetrics.restype = ctypes.c_int


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_pygame_hwnd(pygame_screen):
    """Return the native Windows handle (HWND) of a pygame window.

    Requires SDL2 (pygame >= 2.x).  Raises RuntimeError if running on a
    non-Windows platform.
    """
    if sys.platform != "win32":
        raise RuntimeError("overlay_win is only supported on Windows")

    wm_info = pygame.display.get_wm_info()
    return wm_info["window"]


def _get_screen_size():
    """Return (width, height) of the primary display in pixels."""
    if sys.platform == "win32":
        w = GetSystemMetrics(SM_CXSCREEN)
        h = GetSystemMetrics(SM_CYSCREEN)
    else:
        w, h = 1920, 1080  # fallback for non-Windows
    return w, h


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def apply_overlay(pygame_screen, chroma_key=(0, 0, 0)):
    """Make the given pygame window a borderless, transparent,
    click-through overlay that stays on top.

    Parameters
    ----------
    pygame_screen : pygame.Surface
        The pygame display surface to be modified.
    chroma_key : tuple (R, G, B)
        The colour that will become fully transparent.  Defaults to
        (0, 0, 0) - pure black.

    Returns
    -------
    bool
        True if the overlay was applied, False otherwise (including
        non-Windows platforms).
    """
    if sys.platform != "win32":
        return False

    hwnd = _get_pygame_hwnd(pygame_screen)

    SetWindowLongW(hwnd, GWL_STYLE, WS_POPUP | WS_VISIBLE)

    current_ex = GetWindowLongW(hwnd, GWL_EXSTYLE)
    new_ex = current_ex | WS_EX_LAYERED | WS_EX_TRANSPARENT
    SetWindowLongW(hwnd, GWL_EXSTYLE, new_ex)

    r, g, b = chroma_key
    colorref = (b << 16) | (g << 8) | r
    SetLayeredWindowAttributes(hwnd, colorref, 0, LWA_COLORKEY)

    SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        0,
        0,
        0,
        0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW | SWP_FRAMECHANGED,
    )

    return True


def position_window_bottom_center(pygame_screen):
    """Move the window to the bottom-centre of the primary display.

    Parameters
    ----------
    pygame_screen : pygame.Surface
        The pygame display surface whose window will be repositioned.
    """
    if sys.platform != "win32":
        return

    hwnd = _get_pygame_hwnd(pygame_screen)
    screen_w, screen_h = _get_screen_size()
    win_w = pygame_screen.get_width()
    win_h = pygame_screen.get_height()

    x = (screen_w - win_w) // 2
    y = screen_h - win_h

    SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        x,
        y,
        win_w,
        win_h,
        SWP_SHOWWINDOW,
    )
