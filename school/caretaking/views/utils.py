__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import random

from palettable.colorbrewer import sequential

# path to fonts for wordcloud - TODO move to settings or similar
FONT_PATH = 'C:\Windows\Fonts\Candara.ttf'

### Utils
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """fonts and colours for wordcloud"""
    return tuple(sequential.PuBuGn_9.colors[random.randint(2,8)])

