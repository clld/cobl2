# coding: utf8
from __future__ import unicode_literals, print_function, division

from markdown import markdown
from clld.web.util.helpers import get_referents
from clld_phylogeny_plugin.models import Phylogeny

from cobl2.adapters import CognateClassTree

assert markdown


def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(
        context, exclude=['valueset', 'sentence', 'contribution'])}


def parameter_detail_html(request=None, context=None, **kw):
    return {
        'tree1': CognateClassTree(request, context, Phylogeny.get('1')),
        'tree2': CognateClassTree(request, context, Phylogeny.get('2')),
    }
