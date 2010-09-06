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

"""Helper functions

I assume that you are using SUIT for web templating, as this is how these 
helper functions are approached, although they can probably be adapted for use
with other templating engines such as Mako, Jinja2, etc. with little trouble.

The functions in this module are available to templates via the [call /]
or [transform] rules.  Of course, you should also be able to use these
functions freely in your controller as well with no issues, except perhaps
with `base()`.

For example, if I wanted to fetch a user's IP, I would only have to call:

    [call function="getip" / ]

If I wanted to format some text for Markdown syntax, one would go:
    
    [transform function="converttext" parser="markdown"]*Roar*[/transform]
"""
import re

from pylons import config, request, response, tmpl_context as c
from dateutil import parser as dateutil
from formencode import htmlfill as htmlfill_
from webhelpers.html import literal
from webhelpers.html.converters import textile, nl2br
from markupsafe import Markup
from lxml.html.clean import Cleaner

from phanpy.templating import render
from phanpy.markdown import markdown

__all__ = ['convertdate', 'converttext', 'getip', 'htmlencode', 'htmlfill',
    'slug'
]

htmlencode_re = re.compile('\w')
slug_re = re.compile(r"\W+", re.U)

def base(string, base='base.tpl'):
    """Wrap the current content against a base template."""
    c.content = string
    return render(base)

def converttext(string, parser=''):
    """Takes formatted input to return mark-up based on the given parsers,
    markdown or textile.  If neither are chosen, then the output is sanitized
    (read: unsafe HTML is stripped from the string.)

    **Example Usage**:
        >>> from phanpy.helpers import converttext
        >>> converttext('*Hello*', 'markdown')
        u'<p><em>Hello</em>\n</p>'
    """
    if not parser:
        parser = config.get('phanpy.text.parser', '')
    # Unscape if there is markup so the respective text formatters escape
    # if they deem it necessary.
    string = Markup(string).unescape()
    if parser == 'markdown':
        return markdown.convert(string)
    if parser == 'textile':
        return textile.textile(string, sanitize=True, encoding='utf-8')    
    # Since no parser was selected, return sanitized HTML output with all 
    # unsafe tags and attributes stripped.
    cleaner = Cleaner(add_nofollow=True, comments=True, frames=True,
        forms=True, javascript=True, links=True, meta=True,
        page_structure=True, processing_instructions=True,
        safe_attrs_only=True, style=True, scripts=True
    )
    return cleaner.clean_html(string)

def convertdate(date, format=''):
    """Format a datetime.datetime object or string representation of a date.

    ``date``
        Either a ``string`` or a ``datetime.datetime`` object.  If the latter
        is not provided, then it will assume that the provided ``string`` is a
        date in string format and thus try to parse it with dateutil.

    ``format``
        The desired output format for the date.  If no value is provided, then
        it will use the format specified in the Pylons 
        config (`phanpy.date.format`)
    """
    if not format:
        format = config.get('phanpy.date.format', '%m/%d/%y')
    try:
        return date.strftime(format)
    except AttributeError:
        return dateutil.parse(date).strftime(format)
    except TypeError:
        return _('Unknown')

def getip():
    """Retrieve a client's IP address."""
    return request.environ.get(
        'HTTP_X_FORWARDED_FOR',
        request.environ.get('REMOTE_ADDR', '127.0.0.1')
    )

def htmlencode(string):
    """Converts all of the characters of a string into its equivalent HTML
    entities.
    """
    return literal(''.join(['&#%d;' % ord(x) for x in string]))

def htmlfill(error, form):
    """Convenience function to display FormEncode errors via htmlfill.

        ``error``
            FormEncode error object that is available once
            ``formencode.validators.Invalid`` is raised.
        ``form``
            String containing the HTML document for said form so htmfill may
            display errors.
    """
    return htmlfill_.render(form=form, defaults=request.params,
        errors=(error and error.unpack_errors()),
        encoding=response.determine_charset()
    )

def slug(string):
    """Returns the title converted to all lowercase, and all non-alphanumeric
    characters substitued with a dash.

    ``string``
        The string to format.

    **Example Usage**:
        >>> from phanpy.helpers import slug
        >>> slug('Hello, Gentlemen')
        'hello-gentlemen'
    """
    string = re.sub(
        r'^\W+|\W+$',
        '',
        re.sub(slug_re, '-', string.replace('_', '-'))
    )
    return string.lower()