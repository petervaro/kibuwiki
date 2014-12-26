#!/usr/bin/env python3
## INFO ##
## INFO ##

# Import python modules
import readline
from sys import exit
from itertools import count
from collections import OrderedDict

# Import kibuwiki-dev modules
from doc import Page, Section

# Module level private constants
_fmt = lambda s: '\033[{}m'.format(s)

# Module level public constants
NULL   = _fmt(0)
BOLD   = _fmt(1)
ULINE  = _fmt(4)
HLIGHT = _fmt(7)
STRIKE = _fmt(9)
GRAY   = _fmt(90)
RED    = _fmt(91)
GREEN  = _fmt(92)
YELLOW = _fmt(93)
BLUE   = _fmt(94)
PINK   = _fmt(95)
CYAN   = _fmt(96)
WHITE  = _fmt(97)


#------------------------------------------------------------------------------#
def command(text):
    return YELLOW + BOLD + text + NULL

#------------------------------------------------------------------------------#
def warning(text):
    return RED + text + NULL

#------------------------------------------------------------------------------#
def note(text):
    return CYAN + text + NULL

#------------------------------------------------------------------------------#
def comment(text):
    return GRAY + '### ' + text + NULL


#------------------------------------------------------------------------------#
CTRL = command('\n==> ')
LINE = note('... ')

EMPTY = note('There are no pages saved yet')
MISSING = warning('This feature is not implemented yet')


#------------------------------------------------------------------------------#
class TestApp:

    """
    TestApp is for testing editing and modifying buffers and writing them out to
    the git-repositories. It is based on a very simple finite-state machine.

    First time users should toggle to verbose mode with the 'v' (verbose)
    control option. The verbose mode provides extra hints before each command.
    This could be toggled back anytime.

    TestApp is providing a container for the documents. On start-up is empty,
    but it can be filled by 1) creating new documents 2) loading existing ones
    with the 'l' (load) control option.

    Because TestApp is a FSM, teh user has to switch between the states/layers.
    There are three main layers in TestApp: Void, Page and Section. One can
    check which layer one is using with the '?' (status) control option.

    'Void' layer is, when nothing is open/selected. One can create new pages
    with the 'n' (new) control option, edit their titles with the 'e' (edit)
    control option or completely remove them with the 'd' (delete) control
    option.

    'Page' layer is when a single page has been selected. The user can create
    new sections with the 'n' (new) control option, edit their titles with the
    'e' (edit) control option, completely remove them with the 'd' (delete)
    control option or can return to the 'Void' layer with the 'c' (close)
    control option.

    'Section' layer is when a single page's single section has been selected.
    The user can create new paragraphs with the 'n' (new) control option, edit
    paragraphs with the 'e' (edit) control option, completely remove
    paragraphs with the 'd' (delete) control option or can return to the 'Page'
    layer with the 'c' (close) control option.

    By closing an open page, it will be truncated by default unless the 's'
    (save) control option was passed anytime before the page was closed.

    The 's' (save) control option will only save the currently open/selected
    page into the container of documents. Once the user quits from TestApp, the
    container of documents will be destroyed. Therefore one can use the 'w'
    (write) control option to save changes to the file-system of every document
    of the container of the documents.
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        # Available options
        options = [('h', 'help'   ),
                   ('v', 'verbose'),
                   ('?', 'status' ),
                   ('n', 'new'    ),
                   ('o', 'open'   ),
                   ('c', 'close'  ),
                   ('r', 'read'   ),
                   ('e', 'edit'   ),
                   ('s', 'save'   ),
                   ('d', 'delete' ),
                   ('b', 'browse' ),
                   ('a', 'attach' ),
                   ('l', 'load'   ),
                   ('w', 'write'  ),
                   ('q', 'quit'   ),]

        text = 'OPTIONS: '
        self._help = note(text + ('\n' + ' '*len(text)).join('{} -> {}'.format(*o) for o in options))
        self._options = OrderedDict((c, getattr(self, n)) for c, n in options)

        # States
        self._verbose      = False
        self._open_page    = None
        self._open_section = None

        # Documents
        self._documents = {}


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def run(self):
        # Print options
        print(self._help)
        # Enter main-loop
        while True:
            # If valid control character
            try:
                line = input(CTRL)
                self._options[line]()
            # If invalid control character
            except KeyError:
                if line:
                    print(warning('Invalid control option!'))
                    self.help()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def help(self):
        print(self._help)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def verbose(self):
        self._verbose = not self._verbose
        print(note('verbose -> {!r}'.format('ON' if self._verbose else 'OFF')))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def quit(self):
        print(command('Write files?'))
        if self._verbose:
            print(comment('Any   -> Write changes to files'),
                  comment('Empty -> Do not write changes to files'), sep='\n')
        if input(LINE):
            self.write()
        exit()


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def status(self):
        page = section = None
        try:
            page = self._open_page.title
            section = self._open_section.title
        except AttributeError:
            pass
        # Print status
        print(note('\n'.join(('Open blocks:',
                              '    page:    {!r}'.format(page),
                              '    section: {!r}'.format(section)))))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def attach(self):
        print(MISSING)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def load(self):
        print(MISSING)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def edit(self):
        # If a section is open
        if self._open_section:
            section = self._open_section
            print(note('\n'.join('{: 4} -> {!r}'.format(*p) for p in enumerate(section))))
            print(command('\nEdit paragraph?'))
            if self._verbose:
                print(comment('Index -> Choose a paragraph by its index'),
                      comment('Empty -> Cancel editing'), sep='\n')
            try:
                line  = input(LINE)
                index = int(line)
                section[index]
                print(command('New paragraph?'))
                if self._verbose:
                    print(comment('Text that will replace existing paragraph'))
                section[index] = input(LINE)
            except (IndexError, ValueError):
                if line:
                    print(warning('Invalid paragraph index'))

        # If a page is open
        elif self._open_page:
            page = self._open_page
            print(note('\n'.join('{: 4} -> {.title!r}'.format(*s) for s in enumerate(page))))
            print(command('\nEdit section?'))
            if self._verbose:
                print(comment('Index -> Choose a section by its index'),
                      comment('Empty -> Cancel editing'), sep='\n')
            try:
                line  = input(LINE)
                index = int(line)
                page[index]
                print(command('Section title?'))
                if self._verbose:
                    print(comment('Text that will replace existing section title'))
                page[index].title = input(LINE)
            except (IndexError, ValueError):
                if line:
                    print(warning('Invalid section index'))

        # If nothing is open but there are saved documents
        elif len(self._documents):
            self.browse()
            print(command('\nEdit page?'))
            if self._verbose:
                print(comment('Index -> Choose a page by its identifier'),
                      comment('Empty -> Cancel editing'), sep='\n')
            try:
                page_id = input(LINE)
                self._documents[page_id]
                print(command('Page title?'))
                if self._verbose:
                    print(comment('Text that will replace existing page title'))
                self._documents[page_id].title = input(LINE)
            except KeyError:
                if page_id:
                    print(warning('Invalid page identifier'))

        # If nothing is open and there aren't any documents
        else:
            print(EMPTY)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def browse(self):
        if self._documents:
            print(note('\n'.join('{} -> {.title!r}'.format(*p) for p in self._documents.items())))
        else:
            print(EMPTY)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def new(self):
        """ Create a new page or section """
        # If a section is open
        if self._open_section:
            print(command('New paragraphs?'))
            if self._verbose:
                print(comment('Any   -> Each line is a new paragraph'),
                      comment('Empty -> Escape from editing'), sep='\n')
            line = input(LINE)
            # Read lines
            while line:
                # Create a new paragraph
                self._open_section.add(line)
                line = input(LINE)

        # If a page is open
        elif self._open_page:
            print(command('Section title?'))
            if self._verbose:
                print(comment('Any   -> New section title'),
                      comment('Empty -> Escape from editing'), sep='\n')
            title = input(LINE)
            # Create a new section
            if title:
                self._open_section = section = Section(title)
                self._open_page.add(section)

        # If nothing is open
        else:
            print(command('Page title?'))
            if self._verbose:
                print(comment('Any   -> New page title'),
                      comment('Empty -> Escape from editing'), sep='\n')
            title = input(LINE)
            # Create a new page
            if title:
                # Create a new page
                self._open_page = Page(title)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def close(self):
        # If a section is open
        if self._open_section:
            print(note('Closing opened section: {!r}'.format(self._open_section.title)))
            # Close section
            self._open_section = None

        # If a page is open
        elif self._open_page:
            print(note('Closing opened page: {!r}'.format(self._open_page.title)))
            # Close page
            self._open_page = None

        # If nothing is open
        else:
            print(note('Nothing is open'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def read(self):
        # If any document is open
        try:
            # If section is open
            try:
                print(self._open_section.get())
            # If page is open
            except AttributeError:
                print(self._open_page.get())
        # If nothing is open
        except AttributeError:
            print(note('Nothing is open'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def open(self):
        # If section is open
        if self._open_section:
            print(note('A section is already opened'))

        # If page is open
        elif self._open_page:
            print(note('\n'.join('{: 4} -> {.title}'.format(*s) for s in enumerate(self._open_page))))
            print(command('\nOpen section?'))
            if self._verbose:
                print(comment('Index -> Choose a section by its index'),
                      comment('Empty -> Cancel opening'), sep='\n')
            try:
                line = input(LINE)
                self._open_section = self._open_page[int(line)]
                print(note('Section {!r} is open'.format(self._open_section.title)))
            except (IndexError, ValueError):
                if line:
                    print(warning('No such section in page'))

        # If nothing is open but there are saved documents
        elif len(self._documents):
            self.browse()
            print(command('\nOpen page?'))
            if self._verbose:
                print(comment('Index -> Choose a page by its identifier'),
                      comment('Empty -> Cancel opening'), sep='\n')
            # Open page if valid ID
            try:
                line = input(LINE)
                self._open_page = self._documents[line]
                print(note('Page {!r} is open'.format(self._open_page.title)))
            # If ID is not valid
            except KeyError:
                if line:
                    print(warning('No such page in documents'))

        # If nothing is open and there aren't any documents
        else:
            print(EMPTY)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def save(self):
        # Get local reference
        page = self._open_page
        # Save document if anything is open
        if page:
            page_id = id(page)
            self._documents[str(page_id)] = page
            print(note('Saved: {!r} -> {}'.format(page.title, page_id)))
        else:
            print(note('Nothing to save'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def delete(self):
        # If a section is open
        if self._open_section:
            section = self._open_section
            print(note('\n'.join('{: 4} -> {!r}'.format(*p) for p in enumerate(section))))
            print(command('\nDelete paragraph?'))
            if self._verbose:
                print(comment('Index -> Choose a paragraph by its index'),
                      comment('Empty -> Cancel deleting'), sep='\n')
            try:
                line = input(LINE)
                del section[int(line)]
                print(note('Paragraph removed'))
            except (IndexError, ValueError):
                if line:
                    print(warning('Invalid paragraph index'))

        # If a page is open
        elif self._open_page:
            page = self._open_page
            print(note('\n'.join('{: 4} -> {.title!r}'.format(*s) for s in enumerate(page))))
            print(command('\nDelete section?'))
            if self._verbose:
                print(comment('Index -> Choose a section by its index'),
                      comment('Empty -> Cancel deleting'), sep='\n')
            try:
                line = input(LINE)
                del page[int(line)]
                print(note('Section removed'))
            except (IndexError, ValueError):
                if line:
                    print(warning('Invalid section index'))

        # If nothing is open but there are saved documents
        elif len(self._documents):
            self.browse()
            print(command('\nDelete page?'))
            if self._verbose:
                print(comment('Index -> Choose a page by its identifier'),
                      comment('Empty -> Cancel deleting'), sep='\n')
            try:
                line = input(LINE)
                del self._documents[line]
                print(note('Page removed'))
            except KeyError:
                if line:
                    print(warning('Invalid page identifier'))

        # If nothing is open and there aren't any documents
        else:
            print(EMPTY)


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def write(self):
        print(MISSING)



#------------------------------------------------------------------------------#
if __name__ == '__main__':
    TestApp().run()
