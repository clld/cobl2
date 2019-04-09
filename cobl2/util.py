# coding: utf8
from __future__ import unicode_literals, print_function, division

from markdown import markdown
from clld.web.util.helpers import get_referents
from clld_phylogeny_plugin.models import Phylogeny
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld.db.models.common import Contributor
from clld.db.meta import DBSession
import re

from cobl2.adapters import CognateClassTree

assert markdown

def markdown_remove_links(m):
    return markdown(re.sub(r'\[(.+?)\]\(.+?\)', r'\1', m))

def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(
        context, exclude=['valueset', 'sentence', 'contribution'])}


def parameter_detail_html(request=None, context=None, **kw):
    return {
        'tree1': CognateClassTree(request, context, Phylogeny.get('1')),
        'tree2': CognateClassTree(request, context, Phylogeny.get('2')),
    }

def dataset_detail_html(context=None, request=None, **kw):
    contributor_names = [
        'Cormac Anderson',
        'Erik Anonby',
        'Oleg Belyaev',
        'Hans-Jörg Bibiko',
        'Tonya Kim Dewey-Findell',
        'Cassandra Freiberg',
        'Paul Heggarty',
        'Steve Hewitt',
        'Britta Irslinger',
        'Lechosław Jocz',
        'Ronald Kim',
        'Martin Kümmel',
        'Nikos Liosis',
        'Tijman Pronk',
        'Jakob Runge',
        'Matthew Scarborough',
        'Kim Schulte',
        'Richard Strand',
        'Michiel de Vaan'
    ]
    return {
        'main_contributors': DBSession.query(Contributor)\
                    .filter(Contributor.name.in_(contributor_names))
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

