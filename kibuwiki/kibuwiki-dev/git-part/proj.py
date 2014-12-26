## INFO ##
## INFO ##

# Import kibuwiki modules
from doc import Page

#------------------------------------------------------------------------------#
class Page:
    """
    Abstract Base Class of Pages
    """
    pass



#------------------------------------------------------------------------------#
class WikiPage(Page):
    """
    Base Class of Wiki Pages
    """
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        self._index = Page('Untitled')



#------------------------------------------------------------------------------#
class Tech(WikiPage):
    pass



#------------------------------------------------------------------------------#
class Project(WikiPage):
    pass
