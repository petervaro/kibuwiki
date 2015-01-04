## INFO ##
## INFO ##

# Import python modules
from os import system

# Import pygit2 modules
from pygit2 import (Repository, init_repository, discover_repository,
                    Oid, GIT_FILEMODE_BLOB, Signature, IndexEntry)

# Module level public constants
PATH = 'test-repo'

# Module level private constants
_GITIGNORE = """\
.DS_Store
*.pyc
"""

_README = """\
This is an irrelevant README file :)
"""

# NOTE: There are 4 git-types: blobs, trees, commits and tags
#       Each type can be stored in a Repository and can be accessed by its
#       Oid (Object ID) as they are stored as key-value pairs in the repo.
#

#------------------------------------------------------------------------------#
class Git:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        pass



#------------------------------------------------------------------------------#
def main():

    # HACK: delete everything
    system('rm -rf {}'.format(PATH))

    # If there is an existing repository
    try:
        repo = Repository(discover_repository(PATH))
    # If initialising a new repository
    # TODO: look into the source of pygit2 => this should be a dedicated error
    except KeyError:
        repo = init_repository(PATH)

    # Print what we have
    print('is empty?   =>', repo.is_empty)
    print('path to git =>', repo.path)
    print('path to cwd =>', repo.workdir)
    print('-'*80)

    # Create a .gitignore file (blob)
    oid_of_gitignore = repo.create_blob(_GITIGNORE)
    print('blob   =>', oid_of_gitignore)

    # Create a tree object, and place the blob into it and write it to the repo
    tree = repo.TreeBuilder()
    tree.insert('.gitignore', oid_of_gitignore, GIT_FILEMODE_BLOB)
    oid_of_tree = tree.write()
    print('tree   =>', oid_of_tree)

    # Create a commit
    author = Signature('Peter Varo', 'peter.varo@kitchenbudapest.hu')
    oid_of_commit = repo.create_commit('refs/heads/master',
                                       author, author, 'my first commit',
                                       oid_of_tree, [])
    print('commit =>', oid_of_commit)

    # print(repo.listall_references())
    # print(repo.lookup_reference('HEAD').resolve())

    # print(repo.listall_branches())

    # index = repo.index

    # entry = IndexEntry('.gitignore', oid_of_gitignore, GIT_FILEMODE_BLOB)
    # index.add(entry)
    # print(index['.gitignore'].id)
    # index.write()

    print(repo.status())
    repo.checkout_head()


#------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()
