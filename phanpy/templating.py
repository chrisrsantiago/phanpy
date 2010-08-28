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

import os
import hashlib
import json

from pylons import config, request
import suit

def render(template, **kwargs):
    """Provide our own rendering function for suit-python."""
    filepath = os.path.join(config['pylons.paths']['templates'],
        os.path.normpath(template)
    )
    defaultlog = {'hash': {}, 'contents': []}
    try:
        content = open(filepath).read()
    except IOError:
        raise IOError('Template does not exist: %s' % filepath)
    result = suit.execute(config['suit.rules'], content)

    if 'slacks' in request.params and 'slacks' in kwargs:
        # Granted slacks is enabled for this template and receive a request
        # for slacks, then return JSON'd output instead.
        slacks = json.dumps(suit.log, separators=(',',':'))
        suit.log = defaultlog
        response.headerlist = [
            ('Pragma', 'public'),
            ('Expires', '0'),
            ('Cache-Control', 'must-revalidate, post-check=0, pre-check=0'),
            ('Content-type', 'text/json'),
            ('Content-Disposition', 'attachment; filename=slacks.json'),
            ('Content-Length', len(slacks))
        ]
        suit.log = defaultlog
        return slacks
    return result