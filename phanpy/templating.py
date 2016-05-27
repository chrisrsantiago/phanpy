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

from pylons import config, request, response
import suit

def render(template, rules=None, slacks=False):
    """Load and execute a template file from the template directory based on    
    the rules provided, and optionally enable SLACKS debugging.

    ``template``
        Filename, relative to the project's template directory.  For example,
        >> template = render('template.tpl')
        >> template = render('directory/template.tpl')

    ``rules``
        A dict containing SUIT rules.
        (**Optional**. Default: config['suit.rules'])

    ``slacks``
        Whether or not a SLACKS log is available for download for debugging
        purposes.(**Optional**. Default: False)

        Once this argument is passed, to view a SLACKS log is a simple matter
        of appending the `slacks` querystring to the URL.  For example, assume
        we have a page whose URL is mapped to /index and has SLACKS enabled.
        The URL to request the SLACKS log would be, ``/index?slacks=true``.

        It is also important to note that this argument should only be passed
        once, and only to the "entry point template," which is to say, in
        cases such as:

        >>> class SomeController(BaseController):
        >>>     def index(self):
        >>>         return render('index.tpl', slacks=True)
    """
    filepath = os.path.join(
        config['pylons.paths']['templates'],
        os.path.normpath(template)
    )
    if not rules:
        rules = config['suit.rules']

    try:
        content = open(filepath).read()
    except IOError:
        raise IOError('Template does not exist: %s' % filepath)

    result = suit.execute(rules, content)
    defaultlog = {'hash': {}, 'contents': []}
    if 'slacks' in request.params and slacks:
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
        return slacks
    return result