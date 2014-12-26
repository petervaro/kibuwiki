## INFO ##
## INFO ##

# Module level private constants
_TAB = 4

#------------------------------------------------------------------------------#
class Document:
    """
    Abstract Base Class of Documents
    """
    pass



#------------------------------------------------------------------------------#
class TextDocument(Document):
    """
    Base Class of Text Documents
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __bool__(self):
        return True



#------------------------------------------------------------------------------#
class Page(TextDocument):
    """
    A Page is a collection of Sections
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @property
    def sections(self):
        return self._sections
    @sections.setter
    def sections(self, value):
        self._sections = value


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, title):
        self._title    = title
        self._sections = []


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __len__(self):
        return len(self._sections)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iter__(self):
        for section in self._sections:
            yield section


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __getitem__(self, index):
        return self._sections[index]


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __setitem__(self, index, section):
        self._sections[index] = section


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __delitem__(self, index):
        del self._sections[index]


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add(self, section):
        self._sections.append(section)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def get(self):
        # Build representation
        text = [self._title, '='*len(self._title), '']
        text.extend(s.get(_TAB, i) for i, s in enumerate(self._sections))
        # Return representation
        return '\n'.join(text)



#------------------------------------------------------------------------------#
class Section(TextDocument):
    """
    A Section is a collection of paragraphs
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, title):
        self._title = title
        self._paragraphs = []


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __len__(self):
        return len(self._paragraphs)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __iter__(self):
        for paragraph in self._paragraphs:
            yield paragraph


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __getitem__(self, index):
        return self._paragraphs[index]


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __setitem__(self, index, paragraph):
        self._paragraphs[index] = paragraph


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __delitem__(self, index):
        del self._paragraphs[index]


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add(self, text):
        self._paragraphs.append(text)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def get(self, spaces=0, padding=False):
        text = [''] if padding else []
        text.extend((self._title, '-'*len(self._title), ''))
        text.extend(' '*_TAB + p for p in self._paragraphs)
        # Return representation
        return '\n'.join(' '*spaces + line for line in text)
