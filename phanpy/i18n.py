# Copyright (c) 2010 Chris Santiago (http://faltzershq.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Internationalization (i18n) related functionality to assist in GNU gettext
message extraction via Babel.
"""
import suit
from rulebox.templating import walk

messages = set([])

def extract(fileobj, keywords, comment_tags, options):
    """Extract messages from SUIT template files using Babel.  Original
    extraction code thanks to `Brandon Evans <http://brandonevans.org/>`_.

    ``fileobj``
        The file-like object the messages should be extracted from.

    ``keywords``
        a list of keywords (i.e. function names) that should be recognized as
        translation functions.

    ``comment_tags``
        a list of translator tags to search for and include in the results

    ``options``
        a dictionary of additional options (optional)
    """
    global messages
    rules = {
        '[gettext]': {
            'close': '[/gettext]',
            'functions': [walk, gettext]
        }
    }
    suit.execute(rules, fileobj.read())
    for message in messages:
        yield ('', '[gettext]', message, '')

def gettext(params):
    """Adds a gettext message onto the message set."""
    messages.add(params['string'])
    return params