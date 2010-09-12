import datetime
import unittest

from nose.tools import *

from phanpy import helpers as h

def test_convertdate():
    date_datetime = datetime.datetime(2010, 9, 6, 1, 27, 49, 62000)
    date_string = str(date_datetime)
    format = '%m/%d/%y'
    assert_equal(
        h.convertdate(date_datetime, format=format),
        '09/06/10',
        u'Date conversation for datetime.datetime objects works'
    )
    assert_equal(
        h.convertdate(date_string, format=format),
        '09/06/10',
        u'Date conversation for strings works'
    )

def test_converttext():
    markdown = h.converttext('**Hello World!**', 'markdown')
    textile = h.converttext('*Hello World!*', 'textile')
    html = h.converttext(
        "<p>Hello, I am <strong>very</strong><script>alert('Evil');</script><em>evil</em>.</p>",
        ''
    )

    markdown
    assert_equal(
        markdown,
        u'<p><strong>Hello World!</strong></p>',
        u'Markdown does not work'
    )
    assert_equal(
        textile,
        '<p><strong>Hello World!</strong></p>',
        u'Textile does not work'
    )
    assert_equal(
        html,
        u'<p>Hello, I am <strong>very</strong><em>evil</em>.</p>',
        u'Sanitized HTML does not work'
    )

def test_htmlencode():
    given = 'Hello World!'
    expected = u'&#72;&#101;&#108;&#108;&#111;&#32;&#87;&#111;&#114;&#108;&#100;&#33;'
    assert_equal(h.htmlencode(given), expected)

def test_slug():
    given = 'phanpy can be found @ http://pypi.python.org/phanpy/'
    expected = 'phanpy-can-be-found-http-pypi-python-org-phanpy'
    assert_equal(h.slug(given), expected, u'Slug generation does not work.')