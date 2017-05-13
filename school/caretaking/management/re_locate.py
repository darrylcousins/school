import re

from caretaking.models import Location

# dictionary matching Location name and regex pattern to match
#LOCDICT = {
#        'ABlock': compile('a (and b )?block'),
#        'BBlock': compile('b block'),
#        'Hall': compile('gym|hall'),
#        'HBlock': compile('h block'),
#        'CBlock': compile('c block'),
#        'Math': compile('r(oo)?ms? (17)?/?(18)?'),
#        'English': compile('r(oo)?ms? (19)?/?(20)?'),
#        'Woodshop': compile('wood(shop|work)'),
#        }


class ReLocate:
    """Class to find points from text description
    
    """
    # centre point of school building extent - used if no other location point defined
    college = 'POINT (172.292576 -43.757829)'
    methods = (
        'ABlock',
        'BBlock'
        #'Hall' ,
        #'HBlock',
        #'CBlock',
        #'Math',
        #'English',
        #'Woodshop',
        )

    def __init__(self, text):
        self.text = text

    def compile(self, pattern):
        """return case-insensitive search pattern"""
        return re.compile(pattern, flags=re.IGNORECASE)

    def search(self, pattern):
        return re.search(self.compile(pattern), self.text)

    def get_points(self):
        """
        >>> gp = ReLocate('change bulb in A block')
        >>> gp.get_points()
        >>> gp = ReLocate('change bulbs in A and B block')
        >>> gp.get_points()
        """
        for loc in self.methods:
            matches = getattr(self, loc)()
            print(loc, matches)

    def ABlock(self):
        """
        """
        pattern = 'a (and b )?block'
        return self.search(pattern)

    def BBlock(self):
        """
        """
        pattern = 'b block'
        return self.search(pattern)

