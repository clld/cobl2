# coding: utf8
from __future__ import unicode_literals, print_function, division

from cobl2.adapters import CognateClassTree


def parameter_detail_html(request=None, context=None, **kw):
    return {'tree': CognateClassTree(request, context)}
