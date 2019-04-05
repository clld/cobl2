# coding: utf8
from __future__ import unicode_literals, print_function, division

from markdown import markdown
from clld.web.util.helpers import get_referents
from clld_phylogeny_plugin.models import Phylogeny
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link

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

def cobl_linked_references(req, obj, comments=False):
    chunks = []
    if comments:
        for i, ref in enumerate(sorted(getattr(obj, 'references', []), key=lambda x: x.source.name)):
            if ref.source:
                r = ''
                r += HTML.span(link(req, ref.source), class_='citation')
                d = None
                if ref.description:
                    d = ref.description.split('{')
                    if len(d) == 1:
                        r += HTML.span(": %s" % (d[0] if d[0] else ''), class_='pages')
                    else:
                        r += HTML.span(": %s" % (d[0] if d[0] else ''), class_='pages')
                        if d[1]:
                            r += HTML.blockquote(d[1][:-1])
                chunks.append(HTML.li(r))
        if chunks:
            return HTML.span(*chunks)
    else:
        for i, ref in enumerate(sorted(getattr(obj, 'references', []), key=lambda x: x.source.name)):
            print(vars(ref.source))
            if ref.source:
                if i > 0:
                    chunks.append('; ')
                d = ref.description.split('{')[0] if ref.description else None
                chunks.append(HTML.span(
                    link(req, ref.source),
                    HTML.span(
                        ': %s' % d if d else '',
                        class_='pages'),
                    class_='citation',
                ))
        if chunks:
            return HTML.span(*chunks)
    return ''

