## INFO ##
## INFO ##

# Import python modules
from os.path import join
from random import choice
from string import digits, ascii_lowercase, ascii_uppercase

# Import kibuwiki modules
from project import Project

# Module level public constants
DIR_NAME_LENGTH = 32

# Module level private constants
_CHARS = digits + ascii_lowercase + ascii_uppercase

#------------------------------------------------------------------------------#
def random_string(length):
    return ''.join(choice(_CHARS) for _ in range(length))

#------------------------------------------------------------------------------#
class KiBuWiki:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, location):
        self._index    = join(location, 'data', 'index')
        self._location = location
        self._projects = projects = {}

        # Open projects
        try:
            with open(self._index) as folders:
                for folder in folders:
                    projects[folder] = Project(join(location, 'projects', folder))
        except FileNotFoundError:
            pass

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def add_new_project(self):
        # Generate unique folder-name
        folder = random_string(DIR_NAME_LENGTH)
        while folder in self._projects:
            folder = random_string(DIR_NAME_LENGTH)
        # Return new project object
        return Project(location, 'projects', folder)


kw = KiBuWiki('.')
for i in range(16):
    kw.add_new_project()


"""
kibuwiki
|
+-- data
|   |
|   +-- index
|   |
|   +-- config
|
+-- projects
    |
    +-- ...


Names:
    System: kibuwiki

    Folder : Project
    Files  : Files
    Site   : Page
"""