from clld.web.datatables.base import DetailsRowLinkCol, IdCol, RefsCol, Col, LinkCol, LinkToMapCol, ExternalLinkCol
from clld.web.datatables import value, Languages, Contributors
from clld.web.datatables.contributor import ExternalLinkCol, ContributionsCol, NameCol, UrlCol
from clld.db.models.common import Language, Value, Parameter, Contributor
from clld_cognacy_plugin.datatables import Meanings, Cognatesets, ConcepticonCol
from clld_cognacy_plugin.models import Cognate, Cognateset
from clld.web.util.glottolog import url
from clld.web.util.htmllib import HTML
from clld.db.util import as_int
from clldutils.misc import nfilter
from clld.web.util.helpers import link

from cobl2.models import CognateClass, Meaning, Variety, Lexeme

class CoblMeanings(Meanings):
    def get_options(self):
        opts = super(Meanings, self).get_options()
        opts['aaSorting'] = [[2, 'asc']]
        return opts

    def col_defs(self):
        meaning_cls = list(Parameter.__subclasses__())[0]
        return [
            DetailsRowLinkCol(self, 'more'),
            ConcepticonCol(self, '',
                model_col=getattr(meaning_cls, 'concepticon_id'),
                bSortable=False),
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle="Specification"),
            Col(self,
                'count_languages',
                sTitle='# langs',
                sDescription='number of languages',
                model_col=Meaning.count_languages),
            Col(self,
                'count_lexemes',
                sTitle='# lexemes',
                sDescription='number of lexemes',
                model_col=Meaning.count_lexemes),
            Col(self,
                'count_cognateclasses',
                sTitle='# cognate classes',
                sDescription='number of cognate classes',
                model_col=Meaning.count_cognateclasses),
            Col(self,
                'count_loan_cognateclasses',
                sTitle='# cognate classes (loans)',
                sDescription='number of cognate classes marked as loanword',
                model_col=Meaning.count_loan_cognateclasses),
        ]


class CoblLanguages(Languages):
    def get_default_options(self):
        opts = super(Languages, self).get_default_options()
        opts['iDisplayLength'] = 200,
        return opts

    def col_defs(self):
        return [
            CoblSortIntCol(self, 'sort_order',
                model_col=Variety.sort_order, bSearchable=False),
            CoblCladeCol(self, 'Clade', model_col=Variety.clade),
            LinkCol(self, 'name'),
            Col(self, 'historical', model_col=Variety.historical),
            CoblGlottologCol(self, 'Glottocode', model_col=Variety.glottocode),
            LinkToMapCol(self, 'm'),
            Col(self, 'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self, 'longitude',
                sDescription='<small>The geographic longitude</small>'),
        ]


class CoblSortIntCol(Col):
    __kw__ = {'sTitle': ''}

    def order(self):
        return as_int(self.model_col)

    def format(self, item):
        return ''

class CoblGlottologCol(Col):
    def format(self, item):
        if item.glottocode:
            return HTML.a(item.glottocode, href=url(item.glottocode))
        return ''


class CoblCladeCol(Col):
    def format(self, item):
        # add to clade name the color code as left border
        return '<span style="border-left:12px solid %s;padding-left:5px">%s</span>' % (
            item.color, item.clade)


class CognateClasses(Cognatesets):
    def base_query(self, query):
        return query.outerjoin(Meaning)

    def get_default_options(self):
        opts = super(Cognatesets, self).get_default_options()
        opts['aaSorting'] = [[1, 'asc'],[5, 'desc'],[6, 'desc']]
        return opts

    def col_defs(self):
        return [
            IdCol(self, 'ID', model_col=Cognateset.id, bSortable=False),
            LinkCol(self, 'name', model_col=Meaning.name,
                get_object=lambda cc: cc.meaning_rel,
                sTitle='Meaning'),
            CoblRootFormCol(self, 'Root_form', model_col=CognateClass.root_form),
            Col(self, 'Root_gloss', model_col=CognateClass.root_gloss),
            CoblRootLanguageCol(self, 'Root_language', model_col=CognateClass.root_language),
            Col(self, 'count_clades', model_col=CognateClass.count_clades, sTitle='# clades'),
            Col(self, 'count_lexemes', model_col=CognateClass.count_lexemes, sTitle='# lexemes'),
            Col(self, 'is_loan', model_col=CognateClass.is_loan, sTitle='loan?'),
            Col(self, 'Loan_source', model_col=CognateClass.loan_source_languoid),
            LinkCol(
                self,
                'loaned_from',
                sClass='left',
                model_col=CognateClass.loan_source_pk,
                get_object=lambda cc: cc.loan_source),
            CoblRefsCol(self, 'Source'),
        ]


class CognatesetCol(LinkCol):
    __kw__ = dict(bSearchable=False)

    def order(self):
        return Cognate.cognateset_pk

    def get_obj(self, item):
        return item.cognates[0].cognateset


class CoblRootFormCol(Col):
    def format(self, item):
        if item.root_form:
            return item.root_form
        return '<i>%s</i>' % (item.root_form_calc)


class CoblRootLanguageCol(Col):
    def format(self, item):
        if item.root_language:
            return item.root_language
        return '<i>%s</i>' % (item.root_language_calc)

class CognatesetColorCol(LinkCol):
    __kw__ = dict(bSearchable=False)

    def order(self):
        return Cognate.cognateset_pk

    def get_obj(self, item):
        return item.cognates[0].cognateset

    def format(self, item):
        obj = super(CognatesetColorCol, self).format(item)
        if item.cognates[0].cognateset.color:
            if item.cognates[0].cognateset.root_form_calc or item.cognates[0].cognateset.root_language_calc:
                return '<div style="background-color:%s33;padding:0px 2px;"><i>%s</i></div>' % (
                    item.cognates[0].cognateset.color, obj)
            else:
                return '<div style="background-color:%s33;padding:0px 2px;">%s</div>' % (
                    item.cognates[0].cognateset.color, obj)
        return obj


class CoblFormLanguageCol(LinkCol):
    def format(self, item):
        obj = super(CoblFormLanguageCol, self).format(item)
        # add to language name the color code as left border with tooltip
        return '<span style="border-left:12px solid %s;padding-left:5px" title="Clade: %s">&nbsp;</span>%s' % (
            item.valueset.language.color, item.valueset.language.clade, obj)

class CoblValueRefsCol(value.RefsCol):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        vs = self.get_obj(item)
        return ', '.join(
            nfilter([getattr(vs, 'source', None), cobl_linked_references(self.dt.req, vs)]))

class CoblRefsCol(RefsCol):
    __kw__ = dict(bSearchable=False, bSortable=False)

    def format(self, item):
        vs = self.get_obj(item)
        return ', '.join(
            nfilter([getattr(vs, 'source', None), cobl_linked_references(self.dt.req, vs)]))

class Forms(value.Values):
    def base_query(self, query):
        query = value.Values.base_query(self, query)
        return query.join(Value.cognates).join(Cognate.cognateset)

    def get_default_options(self):
        opts = super(value.Values, self).get_default_options()
        opts['iDisplayLength'] = 200,
        return opts

    def col_defs(self):
        if self.parameter:
            return [
                CoblSortIntCol(self, 'sort_order',
                    model_col=Variety.sort_order, bSearchable=False),
                CoblFormLanguageCol(
                    self,
                    'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
                LinkCol(self, 'name', sTitle='Lexeme'),
                CognatesetColorCol(self, 'cognate_class'),
                Col(self, 'is_loan', model_col=CognateClass.is_loan,
                    get_object=lambda i: i.cognates[0].cognateset, sTitle='loan?'),
                Col(self, 'parallel_loan_event', model_col=CognateClass.parallel_loan_event,
                    get_object=lambda i: i.cognates[0].cognateset, sTitle='pll loan?'),
                Col(self, 'loan_source_languoid', model_col=CognateClass.loan_source_languoid,
                    get_object=lambda i: i.cognates[0].cognateset, sTitle='Source lang'),
                CoblValueRefsCol(self, 'source'),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]
        if self.language:
            return [
                LinkCol(self, 'name', model_col=Meaning.name,
                    get_object=lambda i: i.valueset.parameter,
                    sTitle='Meaning'),
                LinkCol(self, 'name', sTitle='Lexeme'),
                Col(self, 'native_script', model_col=Lexeme.native_script),
                CognatesetCol(self, 'cognate_class'),
                Col(self, 'is_loan', model_col=CognateClass.is_loan,
                    get_object=lambda i: i.cognates[0].cognateset, sTitle='loan?'),
                Col(self, 'parallel_loan_event', model_col=CognateClass.parallel_loan_event,
                    get_object=lambda i: i.cognates[0].cognateset, sTitle='pll loan?'),
                CoblValueRefsCol(self, 'source'),
            ]
        return value.Values.col_defs(self)


class CoblContributors(Contributors):
    def col_defs(self):
        return [
            CoblAuthorNameCol(self, 'name'),
            ContributionsCol(self, 'Contributions'),
            UrlCol(self, 'Homepage'),
        ]


class CoblAuthorNameCol(LinkCol):
    def order(self):
        return Contributor.pk


def cobl_linked_references(req, obj):
    chunks = []
    for i, ref in enumerate(sorted(getattr(obj, 'references', []),
            key=lambda x: x.source.name if x and x.source and x.source.name else '')):
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


def includeme(config):
    #
    # Note: We cannot register CognateClasses here, because this includeme is run when
    # the clld core app is included, and *before* the clld-cognacy-plugin is included.
    # Thus, the registration would be overwritten. The solution is to register the table
    # "manually", i.e. in cobl2.main.
    #
    config.register_datatable('values', Forms)
    config.register_datatable('cognatesets', CognateClasses)
    config.register_datatable('parameters', CoblMeanings)
    config.register_datatable('languages', CoblLanguages)
    config.register_datatable('contributors', CoblContributors)
