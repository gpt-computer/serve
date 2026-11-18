"""Terminal/Rich console helpers for colored output."""

import os
from typing import List, Optional, Union

from rich.console import Console

from gptc.constants import __windows__

_COLORS = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}

_HIGHLIGHTS = {
    "on_grey": 40,
    "on_red": 41,
    "on_green": 42,
    "on_yellow": 43,
    "on_blue": 44,
    "on_magenta": 45,
    "on_cyan": 46,
    "on_white": 47,
}

_ATTRIBUTES = {
    "bold": 1,
    "dark": 2,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "concealed": 8,
}

_RESET = "\033[0m"

if __windows__:  # pragma: no cover
    os.system("color")


def colored(
    text: str,
    color: Optional[str] = None,
    on_color: Optional[str] = None,
    attrs: Optional[Union[str, list]] = None,
) -> str:
    """
    Give the text with color.

    :param text: The target text.
    :param color: The color of text. Chosen from the following.
        {
            'grey': 30,
            'red': 31,
            'green': 32,
            'yellow': 33,
            'blue': 34,
            'magenta': 35,
            'cyan': 36,
            'white': 37
        }
    :param on_color: The on_color of text. Chosen from the following.
        {
            'on_grey': 40,
            'on_red': 41,
            'on_green': 42,
            'on_yellow': 43,
            'on_blue': 44,
            'on_magenta': 45,
            'on_cyan': 46,
            'on_white': 47
        }
    :param attrs: Attributes of color. Chosen from the following.
       {
          'bold': 1,
          'dark': 2,
          'underline': 4,
          'blink': 5,
          'reverse': 7,
          'concealed': 8
       }
    :return: Colored text.
    """
    if "GPTC_LOG_NO_COLOR" not in os.environ:
        fmt_str = "\033[%dm%s"
        if color:
            text = fmt_str % (_COLORS[color], text)
        if on_color:
            text = fmt_str % (_HIGHLIGHTS[on_color], text)

        if attrs:
            if isinstance(attrs, str):
                attrs = [attrs]
            if isinstance(attrs, list):
                for attr in attrs:
                    text = fmt_str % (_ATTRIBUTES[attr], text)
        text += _RESET
    return text


def colored_rich(
    text: str,
    color: Optional[str] = None,
    on_color: Optional[str] = None,
    attrs: Optional[Union[str, list]] = None,
) -> str:
    """
    Give the text with color. You should only use it when printing with rich print. Othersiwe please see the colored
    function

    :param text: The target text
    :param color: The color of text
    :param on_color: The on color of text: ex on yellow
    :param attrs: Attributes of color

    :return: Colored text.
    """
    if "GPTC_LOG_NO_COLOR" not in os.environ:
        if color:
            text = _wrap_text_in_rich_bracket(text, color)
        if on_color:
            text = _wrap_text_in_rich_bracket(text, on_color)

        if attrs:
            if isinstance(attrs, str):
                attrs = [attrs]
            if isinstance(attrs, list):
                for attr in attrs:
                    text = _wrap_text_in_rich_bracket(text, attr)
    return text


def _wrap_text_in_rich_bracket(text: str, wrapper: str):
    return f"[{wrapper}]{text}[/{wrapper}]"


def get_rich_console() -> Console:
    """Return a singleton :class:`rich.console.Console` instance."""
    return Console()
