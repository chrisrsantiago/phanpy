"""A set of some rather useful rules for SUIT."""
import hashlib

from pylons import config, tmpl_context as c
from rulebox import templating, suitlons
import suit

def gravatar(params):
    """Return a Gravatar for the given email address."""
    email_hash = hashlib.md5(params['string']).hexdigest()
    rating = params['var']['rating']
    size = params['var']['size']
    format = 'http://www.gravatar.com/avatar/%s?r=%s&s=%s'
    c._gravatar = format % (email_hash, rating, size)
    params['string'] = suit.execute(suitlons.rules, params['var']['markup'])
    return params

def replace(params):
    """Replace in a string."""
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
                'size': config.get('phanpy.gravatar.size', '80')
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