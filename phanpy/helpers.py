"""Helper functions

I assume that you are using SUIT for web templating, as this is how these 
helper functions are approached, although they can probably be adapted for use
with other templating engines such as Mako, Jinja2, etc. with little trouble.

The functions in this module are available to templates via the [call /]
or [transform] rules.

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

__all__ = ['convertdate', 'converttext', 'getip', 'htmlfill']

def base(string, base='base.tpl'):
    """Wrap the current content against a base template."""
    c.content = string
    return render(base)

def converttext(string, parser=''):
    """Takes formatted input to return mark-up based on the given parsers,
    markdown or textile.  If neither are chosen, sanitized HTML is instead 
    returned.
    """
    if not parser:
        parser = config['phanpy.text.parser']
    string = Markup(string).unescape()
    if parser == 'markdown':
        return markdown.convert(string)
    if parser == 'textile':
        return textile(string, sanitize=True, encoding='utf-8')    
    # Since no parser was selected, return sanitized HTML output instead.
    cleaner = Cleaner(add_nofollow=True, comments=True, frames=True,
        forms=True, javascript=True, links=True, meta=True,
        page_structure=True, processing_instructions=True,
        safe_attrs_only=True, style=True, scripts=True
    )
    return cleaner.clean_html(string)

def convertdate(date, format=''):
    """Convert a datetime.datetime into string representation using the date
    settings specified in the configuration INI file or by the format argument.
    """
    if not format:
        format = config['phanpy.date.format']
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

def slug(string):
    """Returns the title converted to all lowercase, and all non-alphanumeric
    characters substitued with a dash.
    """
    regex = re.compile(r"\W+", re.U)
    string = re.sub(
        r'^\W+|\W+$',
        '',
        re.sub(regex, '-', string.replace('_', '-'))
    )
    return string.lower()

def htmlfill(error, form):
    """Convenience function to display FormEncode errors via htmlfill."""
    return htmlfill_.render(form=form, defaults=request.params,
        errors=(error and error.unpack_errors()),
        encoding=response.determine_charset()
    )