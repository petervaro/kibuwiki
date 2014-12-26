## INFO ##
## INFO ##

from itertools import chain

import pygit2

FULL_REPO_PATH = 'test_full_repo'
BARE_REPO_PATH = 'test_bare_repo'

def get_repo(path, bare=False):
    try:
        return pygit2.Repository(pygit2.discover_repository(path))
    except KeyError:
        return pygit2.init_repository(path, bare=bare)

full_repo = get_repo(FULL_REPO_PATH)
bare_repo = get_repo(BARE_REPO_PATH, bare=True)

print(full_repo, bare_repo, sep='\n')

# Create Tree objects
full_tree_builder = full_repo.TreeBuilder()
bare_tree_builder = bare_repo.TreeBuilder()

SAMPLE_TEXT = 'this is a test file'
full_file_id = full_repo.create_blob(SAMPLE_TEXT)
bare_file_id = bare_repo.create_blob(SAMPLE_TEXT)

FILE_NAME = 'test_file1'
full_tree_builder.insert(FILE_NAME, full_file_id, pygit2.GIT_FILEMODE_BLOB)
bare_tree_builder.insert(FILE_NAME, bare_file_id, pygit2.GIT_FILEMODE_BLOB)

full_tree_builder.write()
bare_tree_builder.write()

for entry in chain(full_tree, bare_tree):
    print(entry.id, entry.name)
