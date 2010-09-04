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

"""A set of some rather useful rules for SUIT.  I am assuming you have read
the SUIT documentation to know the most basic concepts to use these rules,
so I will not bother getting into that.  If you have not read the
`documentation <http://www.python.org/>`_, then now is the time.

Usage in a Pylons setting would look something like this:
  >>> import suit
  >>> from rulebox import suitlons
  >>> from phanpy.rules import rules as phanpy
  >>> rules = dict(suitlons.rules.copy(), **phanpy.copy())
  >>> suit.execute(rules, '[gravatar]myemail@domain.com[/gravatar]')
"""
import hashlib

from pylons import config, tmpl_context as c
from rulebox import templating, suitlons
import suit

def gravatar(params):
    """Return a Gravatar for the given email address.

    **Syntax:**
        [gravatar]email[/gravatar]

    **Attributes**
        ``markup``
            What the markup for the given Gravatar should be once generated.
            The URL for the Gravatar is available as [c]_gravatar[/c].
            (**Optional**.  Default: `<img src="[c]_gravatar[/c]" alt="">`)

        ``rating``
            The rating for the given Gravatar. (**Optional**. Default: PG)

        ``size``
            The size for the given Gravatar. (**Optional**. Default: 80)

        ``default``
            The default image to use if the given email address does not have
            a Gravatar. (**Optional**. Default: identicon)
    """
    email_hash = hashlib.md5(params['string']).hexdigest()
    rating = params['var']['rating']
    size = params['var']['size']
    default = params['var']['default']
    format = 'http://www.gravatar.com/avatar/%s?r=%s&s=%s&d=%s'
    c._gravatar = format % (email_hash, rating, size, default)
    params['string'] = suit.execute(suitlons.rules, params['var']['markup'])
    return params

def replace(params):
    """Replace in a string.  This function works the same exact way a string
    replace operation would work with the ``.replace()`` method.

    **Syntax:**
        [replace]string[/replace]

    **Attributes**
        ``what``
            Substring to replace. (**Required**.)

        ``with``
            The replacement for every occurance of ``what``. (**Required**)
    """
    params['string'] = params['string'].replace(
        params['var']['what'],
        params['var']['with']
    )
    return params

rules = {
    '[gravatar]':
    {
        'close': '[/gravatar]',
        'functions': [templating.walk, templating.attribute, gravatar],
        'var':
        {
            'equal': templating.default['equal'],
            'log': templating.default['log'],
            'quote': templating.default['quote'],
            'var':
            {
                'markup': '<img src="[c]_gravatar[/c]" alt="">',
                'rating': config.get('phanpy.gravatar.rating', 'PG'),
                'size': config.get('phanpy.gravatar.size', '80'),
                'default': config.get('phanpy.gravatar.default', 'identicon')
            }
        }
    },
    '[gravatar':
    {
        'close': ']',
        'create': '[gravatar]',
        'skip': True
    },
    '[replace]':
    {
        'close': '[/replace]',
        'functions': [templating.walk, templating.attribute, replace],
        'var':
        {
            'equal': templating.default['equal'],
            'log': templating.default['log'],
            'quote': templating.default['quote'],
            'var':
            {
                'what': '',
                'with': ''
            }
        }
    },
    '[replace':
    {
        'close': ']',
        'create': '[replace]',
        'skip': True
    }
}