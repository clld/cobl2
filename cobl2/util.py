from markdown import markdown
from clld.web.util.helpers import get_referents
from clld_phylogeny_plugin.models import Phylogeny
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import link
from clld.web.util.multiselect import MultiSelect
from clld.db.models.common import Contributor
from clld.db.meta import DBSession
from cobl2.models import Variety, Author, Policie, CognateClass
import re

from cobl2.adapters import CognateClassTree

assert markdown


def markdown_handle_links(req, m):
    for lnk in re.findall(r'(\[(.+?)\]\(.+?\))', m):
        # create links to parameters/...
        if 'wiki/Meaning:-' in lnk[0]:
            m = m.replace(lnk[0], link(req, lnk[1], rsc='parameter', label=lnk[1]))
        # delete links
        else:
            m = m.replace(lnk[0], lnk[1])
    return markdown(m.replace('\\n', '\n'))


def markdown_policies(m):
    return markdown(m.replace('\\n', '\n'))


def table_of_policies(request):
    q = DBSession.query(Policie.name, Policie.id).order_by(Policie.pk).all()
    r = []
    r.append(HTML.h4('Table of Policies:'))
    for name, id in q:
        r.append(HTML.a(name, href='%s/%s' % (request.route_url('policies'), id)))
        r.append(HTML.br())
    return ''.join(r)


def policie_index_html(context=None, request=None, **kw):
    return {'table_of_policies': table_of_policies(request)}


def policie_detail_html(context=None, request=None, **kw):
    return {'table_of_policies': table_of_policies(request)}


def source_detail_html(context=None, request=None, **kw):
    return {'referents': get_referents(
        context, exclude=['valueset', 'sentence', 'contribution'])}


class CladeMultiSelect(MultiSelect):
    def __init__(self, ctx, req, name='cladefilter', eid='ms-cladefilter', **kw):
        if ctx.cladefilter and len(ctx.cladefilter[0]):
            kw['selected'] = ctx.cladefilter
        else:
            kw['selected'] = None
        MultiSelect.__init__(self, req, name, eid, **kw)

    def format_result(self, obj):
        o = '%s' % (getattr(obj, 'label', obj))
        return {'id': o, 'text': o}

    @classmethod
    def query(cls):
        return DBSession.query(Variety.clade_name).distinct().order_by(Variety.clade_name)

    def get_options(self):
        return {
            'data': [self.format_result(p) for p in self.query()],
            'multiple': True}


def cognateset_index_html(context=None, request=None, **kw):
    return dict(select=CladeMultiSelect(context, request))


def cognateset_snippet_html(context=None, request=None, **kw):
    return {'revisors': get_revisors(context, request)}


def cognateset_detail_html(context=None, request=None, **kw):
    return {'revisors': get_revisors(context, request)}


def get_revisors(context=None, request=None, **kw):
    res = []
    if not context.revised_by:
        return None
    for r in context.revised_by.split(','):
        for f in DBSession.query(Author).filter(Author.id == r):
            res.append(HTML.a(f.name, href='%s/%s' % (request.route_url('contributors'), r)))
    return ', '.join(res)


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
        'main_contributors': DBSession.query(Contributor).filter(
            Contributor.name.in_(contributor_names))
    }


def cobl_linked_cognateclass(req, obj):
    return HTML.span((HTML.i if obj.root_form_calc else HTML.span)
                     (link(req, obj)), style="background-color:{0}33".format(obj.color))


def cobl_linked_references(req, obj, comments=False):
    chunks = []
    if comments:
        for i, ref in enumerate(sorted(getattr(obj, 'references', []), key=lambda x: x.source.name or '')):
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
        for i, ref in enumerate(sorted(getattr(obj, 'references', []), key=lambda x: x.source.name or '')):
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
