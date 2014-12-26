#!/usr/bin/env python
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
CTRL = command('\n==> ')
LINE = note('... ')


#------------------------------------------------------------------------------#
class TestApp:

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self):
        # Available options
        options = [('h', 'help'  ),
                   ('?', 'status'),
                   ('n', 'new'   ),
                   ('o', 'open'  ),
                   ('c', 'close' ),
                   ('r', 'read'  ),
                   ('e', 'edit'  ),
                   ('s', 'save'  ),
                   ('d', 'delete'),
                   ('b', 'browse'),
                   ('a', 'attach'),
                   ('w', 'write' ),
                   ('q', 'quit'  ),]

        text = 'OPTIONS: '
        self._help = note(text + ('\n' + ' '*len(text)).join('{} -> {}'.format(*o) for o in options))
        self._options = OrderedDict((c, getattr(self, n)) for c, n in options)

        # States
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
    def quit(self):
        print(command('Write files?'))
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
        pass


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def edit(self):
        # If a section is open
        if self._open_section:
            section = self._open_section
            print(note('\n'.join('{: 4} -> {!r}'.format(*p) for p in enumerate(section))))
            print(command('\nEdit paragraph?'))
            try:
                index = int(input(LINE))
                section[index]
                print(command('New paragraph?'))
                section[index] = input(LINE)
            except (IndexError, ValueError):
                print(warning('Invalid paragraph index'))

        # If a page is open
        elif self._open_page:
            page = self._open_page
            print(note('\n'.join('{: 4} -> {.title!r}'.format(*s) for s in enumerate(page))))
            print(command('\nEdit section?'))
            try:
                index = int(input(LINE))
                page[index]
                print(command('Section title?'))
                page[index].title = input(LINE)
            except (IndexError, ValueError):
                print(warning('Invalid section index'))

        # If nothing is open but there are saved documents
        elif len(self._documents):
            self.browse()
            print(command('\nEdit page?'))
            try:
                page_id = input(LINE)
                self._documents[page_id]
                print(command('Page title?'))
                self._documents[page_id].title = input(LINE)
            except KeyError:
                print(warning('Invalid page identifier'))

        # If nothing is open and there aren't any documents
        else:
            print(note('Documents are empty'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def browse(self):
        print(note('\n'.join('{} -> {.title!r}'.format(*p) for p in sorted(self._documents.items()))))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def new(self):
        """ Create a new page or section """
        # If a section is open
        if self._open_section:
            print(command('New paragraphs?'))
            line = input(LINE)
            # Read lines
            while line:
                # Create a new paragraph
                self._open_section.add(line)
                line = input(LINE)

        # If a page is open
        elif self._open_page:
            print(command('Section title?'))
            title = input(LINE)
            # Create a new section
            if title:
                self._open_section = section = Section(title)
                self._open_page.add(section)

        # If nothing is open
        else:
            print(command('Page title?'))
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
            try:
                self._open_section = self._open_page[int(input(LINE))]
                print(note('Section {!r} is open'.format(self._open_section.title)))
            except (IndexError, ValueError):
                print(warning('No such section in page'))

        # If nothing is open but there are saved documents
        elif len(self._documents):
            self.browse()
            print(command('\nOpen page?'))
            # Open page if valid ID
            try:
                self._open_page = self._documents[input(LINE)]
                print(note('Page {!r} is open'.format(self._open_page.title)))
            # If ID is not valid
            except KeyError:
                print(warning('No such page in documents'))

        # If nothing is open and there aren't any documents
        else:
            print(note('Documents are empty'))


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
            print(note('Nothing is open, therefore nothing is saved'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def delete(self):
        # If a section is open
        if self._open_section:
            section = self._open_section
            print(note('\n'.join('{: 4} -> {!r}'.format(*p) for p in enumerate(section))))
            print(command('\nDelete paragraph?'))
            try:
                del section[int(input(LINE))]
                print(note('Paragraph removed'))
            except (IndexError, ValueError):
                print(warning('Invalid paragraph index'))

        # If a page is open
        elif self._open_page:
            page = self._open_page
            print(note('\n'.join('{: 4} -> {.title!r}'.format(*s) for s in enumerate(page))))
            print(command('\nDelete section?'))
            try:
                del page[int(input(LINE))]
                print(note('Section removed'))
            except (IndexError, ValueError):
                print(warning('Invalid section index'))

        # If nothing is open but there are saved documents
        elif len(self._documents):
            self.browse()
            print(command('\nDelete page?'))
            try:
                del self._documents[input(LINE)]
                print(note('Page removed'))
            except KeyError:
                print(warning('Invalid page identifier'))

        # If nothing is open and there aren't any documents
        else:
            print(note('Documents are empty'))


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def write(self):
        pass



#------------------------------------------------------------------------------#
if __name__ == '__main__':
    TestApp().run()
