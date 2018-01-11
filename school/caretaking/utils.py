__author__ = 'Darryl Cousins <darryljcousins@gmail.com>'

import re
from collections import deque

from django.db.models import Q

class QueryBuilder:
    """
    Build complex queries from a search string using `and`, `or`, and `not`::

        >>> s = '(grafitti or graffiti) and boys and not girls'
        >>> qb = QueryBuilder(s, 'description')

    """
    special_words = ['not', 'and', 'or']

    def __init__(self, search_string='', field_name=''):
        self.parts = deque(self.split_search_string(search_string))
        self.field_name = field_name
        self.words = []
        self.query = Q()

    def parse_parts(self):
        """
        Run through the parts, group accordingly and create query object.

            >>> s = 'graf*'
            >>> qb = QueryBuilder(s, 'text')
            >>> qb.parse_parts()
            >>> print(qb.query)
            >>> print(qb.words)

        """
        parts = self.parts.copy()
        while parts:
            word = parts.popleft()
            # a straight word to search on
            if word not in self.special_words:
                self.word(word)
            # create a negated query
            elif word == 'not':
                try:
                    # get the next word
                    next_word = parts.popleft()
                    # check that it is not a special word
                    if next_word not in self.special_words:
                        # create a 'not' Q object
                        self.qb_not(next_word)
                    else:
                        # if a special word: ignore, reinsert and carry on
                        parts.appendleft(next_word)
                except IndexError:
                    # fail silently if no words to follow
                    pass
            # create an or query
            elif word == 'or':
                try:
                    # get the next word
                    next_word = parts.popleft()
                    # check that it is not a special word
                    if next_word not in self.special_words:
                        # create a 'or' Q object
                        self.qb_or(next_word)
                    else:
                        # if a special word: ignore, reinsert and carry on
                        parts.appendleft(next_word)
                except IndexError:
                    # fail silently if no words to follow
                    pass
            # create an and query
            elif word == 'or':
                try:
                    # get the next word
                    next_word = parts.popleft()
                    # check that it is not a special word
                    if next_word not in self.special_words:
                        # create an 'and' Q object
                        self.word(next_word)
                    elif next_word == 'not':
                        # create a 'not' Q object
                        self.qb_not(next_word)
                    else:
                        # if a special word: ignore, reinsert and carry on
                        parts.appendleft(next_word)
                except IndexError:
                    # fail silently if no words to follow
                    pass

        pass

    def word(self, word):
        """Creates an AND query"""
        self.words.append(word)
        self.query &= Q(**{'{}__icontains'.format(self.field_name): word})

    def qb_or(self, word):
        self.words.append(word)
        self.query |= Q(**{'{}__icontains'.format(self.field_name): word})

    def qb_not(self, word):
        self.words.append('~' + word)
        self.query &= ~Q(**{'{}__icontains'.format(self.field_name): word})

    def split_search_string(self, s):
        """
        Split a search string to find relevant parts.

            >>> qb = QueryBuilder()
            >>> s = 'grafitti or graffiti'
            >>> qb.split_search_string(s)
            ['grafitti', 'or', 'graffiti']

            >>> s = '(grafitti or graffiti) and hall'
            >>> qb = QueryBuilder()
            >>> qb.split_search_string(s)
            ['(', 'grafitti', 'or', 'graffiti', ')', 'and', 'hall']

        """
        return [part for part in [p.strip() for p in re.compile(r'([\w\*]+)').split(s)] if part]
