from clld.web.datatables.base import (
    DataTable, DetailsRowLinkCol,
    IdCol, RefsCol, Col, LinkCol,
    LinkToMapCol, ExternalLinkCol)
from clld.web.datatables import value, Languages, Contributors, Sources
from clld.web.datatables.contributor import (
    ExternalLinkCol, ContributionsCol, NameCol, UrlCol)
from clld.db.models.common import (
    Language, Value, Parameter,
    Contributor, ValueSet, ValueSetReference)
from clld_cognacy_plugin.datatables import Meanings, Cognatesets, ConcepticonCol
from clld_cognacy_plugin.models import Cognate, Cognateset
from clld.web.util.glottolog import url
from clld.web.util.htmllib import HTML
from clld.db.util import as_int, get_distinct_values, icontains
from clldutils.misc import nfilter
from clld.web.util.helpers import link, button
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from cobl2.models import CognateClass, Meaning, Variety, Lexeme, Clade


class CoblClades(DataTable):
    def get_options(self):
        opts = super(DataTable, self).get_options()
        opts['aaSorting'] = [[0, 'asc']]
        return opts

    def col_defs(self):
        return [
            CoblSortIntCol(self, 'pk', bSearchable=False),
            Col(self, 'clade_level0', sTitle='Cl 0', sTooltip='clade level 0',
                bSearchable=False),
            Col(self, 'level0_name', sTitle='Clade 0 name'),
            Col(self, 'clade_level1', sTitle='Cl 1', sTooltip='clade level 1',
                bSearchable=False),
            Col(self, 'level1_name', sTitle='Clade 1 name'),
            Col(self, 'clade_level2', sTitle='Cl 2', sTooltip='clade level 2',
                bSearchable=False),
            Col(self, 'level2_name', sTitle='Clade 2 name'),
            Col(self, 'clade_level3', sTitle='Cl 3', sTooltip='clade level 3',
                bSearchable=False),
            Col(self, 'level3_name', sTitle='Clade 3 name'),
            CoblCladeNameCol(self, 'clade_name'),
            CoblFilterCladeNameCol(self, 'short_name', sTitle='Clade'),
            Col(self, 'at_most', sTitle='At most?',
                sTooltip='Latest plausible date at which divergence had not yet begun'),
            Col(self, 'at_least', sTitle='At least?',
                sTooltip='Earliest plausible date divergence could have begun by'),
        ]


class CoblFilterCladeNameCol(Col):
    __kw__ = dict(bSearchable=False, bSortable=False)
    def format(self, item):
        if item.short_name:
            return item.clade_name
        return ''


class CoblCladeNameCol(Col):
    def format(self, item):
        # add to clade name the color code as left border
        return '<span style="border-left:12px solid %s;padding-left:5px">%s</span>' % (
            item.color, item.clade_name)


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
            Col(self,
                'count_languages',
                sTitle='# langs',
                sTooltip='number of languages per meaning',
                model_col=Meaning.count_languages),
            Col(self,
                'count_lexemes',
                sTitle='# lexemes',
                sTooltip='number of lexemes per meaning',
                model_col=Meaning.count_lexemes),
            Col(self,
                'count_cognateclasses',
                sTitle='# cognate sets',
                sTooltip='number of cognate sets per meaning',
                model_col=Meaning.count_cognateclasses),
            Col(self,
                'count_loan_cognateclasses',
                sTitle='# loans',
                sTooltip='number of cognate sets marked as loan event',
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
            BoolCol(self, 'historical', model_col=Variety.historical),
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
    def __init__(self, req, *args, **kw):
        Cognatesets.__init__(self, req, *args, **kw)
        self.cladefilter = None
        if 'cladefilter' in req.params:
            self.cladefilter = req.params['cladefilter'].split(',')

    def base_query(self, query):
        query = query.outerjoin(Meaning)
        if self.cladefilter:
            q = [icontains(CognateClass.clades, q) for q in self.cladefilter]
            query = query.filter(and_(*q))
        return query.distinct()

    def get_default_options(self):
        opts = super(Cognatesets, self).get_default_options()
        opts['aaSorting'] = [[1, 'asc'],[4, 'desc'],[5, 'desc']]
        return opts

    def col_defs(self):
        return [
            IdCol(self, 'ID', model_col=Cognateset.id, bSortable=False),
            LinkCol(self, 'name', model_col=Meaning.name,
                get_object=lambda cc: cc.meaning_rel,
                sTitle='Meaning'),
            CoblRootFormCol(self, 'Root_form', model_col=CognateClass.root_form),
            CoblRootLanguageCol(self, 'Root_language', model_col=CognateClass.root_language,
                sTitle='Root ref. language',
                sTooltip='Root reference language'),
            CoblCladesCol(self, 'count_clades', model_col=CognateClass.count_clades,
                sTitle='# clades',
                sTooltip='number of general clades found in cogante set',),
            Col(self, 'count_lexemes', model_col=CognateClass.count_lexemes,
                sTitle='# lexemes',
                sTooltip='number of lexemes per cognate set',),
            BoolCol(self, 'is_loan', model_col=CognateClass.is_loan,
                sTitle='loan?',
                sTooltip='is cognate set marked as loan event'),
            BoolCol(self, 'parallel_loan_event', model_col=CognateClass.parallel_loan_event,
                sTitle='pll loan?',
                sTooltip='is cognate set marked as parallel loan event'),
            Col(self, 'Loan_source', model_col=CognateClass.loan_source_languoid),
            LinkCol(
                self,
                'loaned_from',
                sClass='left',
                model_col=CognateClass.loan_source_pk,
                get_object=lambda cc: cc.loan_source),
            DetailsRowLinkCol(self, 'more'),
        ]


class CoblCladesCol(Col):
    def format(self, item):
        colors = []
        for c in item.involved_clade_colors.split(' '):
            if c == '0':
                colors.append('<div class="clade-col-block-item-white"></div>')
            else:
                colors.append('<div class="clade-col-block-item" style="background-color:%s;"></div>' % (c))
        return('<div style="display:block;">%i<span class="clade-col-block" title="Involved general clades:\n%s">%s</span></div>' % (
                item.count_clades,
                item.clades,
                ''.join(colors)
            ))


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

class CoblFormSelectCladeNameCol(Col):
    def search(self, qs):
        q = [self.model_col.__eq__(q) for q in qs.split(',')]
        return or_(*q)

class CoblFormSelectLanguageCol(CoblFormLanguageCol):
    def search(self, qs):
        q = [self.model_col.__eq__(q) for q in qs.split(',')]
        return or_(*q)

class CoblFormSelectMeaningCol(LinkCol):
    def search(self, qs):
        q = [self.model_col.__eq__(q) for q in qs.split(',')]
        return or_(*q)

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
        if not self.parameter and not self.language:
            return query.join(Value.cognates).join(Cognate.cognateset)\
                .join(ValueSet.parameter).join(ValueSet.language).options(
                    joinedload(Value.cognates),
                    joinedload(Value.cognates, Cognate.cognateset),
                    joinedload(Value.valueset, ValueSet.parameter),
                    joinedload(Value.valueset, ValueSet.language)
                )
        else:
            return query.join(Value.cognates).join(Cognate.cognateset).options(
                    joinedload(Value.cognates),
                    joinedload(Value.cognates, Cognate.cognateset))

    def get_default_options(self):
        opts = super(value.Values, self).get_default_options()
        opts['iDisplayLength'] = 200,
        if not self.parameter and not self.language:
            opts['aaSorting'] = [[0, 'asc'], [2, 'asc'], [5, 'asc']]
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
                CognatesetColorCol(self, 'cognate_class', sTitle='Cognate set'),
                BoolCol(self, 'is_loan', model_col=CognateClass.is_loan,
                    get_object=lambda i: i.cognates[0].cognateset,
                    sTitle='loan?', sTooltip='is cognate set marked as loan event'),
                BoolCol(self, 'parallel_loan_event', model_col=CognateClass.parallel_loan_event,
                    get_object=lambda i: i.cognates[0].cognateset,
                    sTitle='pll loan?', sTooltip='is cognate set marked as parallel loan event'),
                Col(self, 'loan_source_languoid', model_col=CognateClass.loan_source_languoid,
                    get_object=lambda i: i.cognates[0].cognateset, sTitle='Source lang'),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
                DetailsSourceRowLinkCol(self, 'source', button_text='source', sTitle='Source')
            ]
        if self.language:
            return [
                LinkCol(self, 'name', model_col=Meaning.name,
                    get_object=lambda i: i.valueset.parameter,
                    sTitle='Meaning'),
                LinkCol(self, 'name', sTitle='Lexeme'),
                Col(self, 'native_script', model_col=Lexeme.native_script),
                CognatesetCol(self, 'cognate_class', sTitle='Cognate set'),
                BoolCol(self, 'is_loan', model_col=CognateClass.is_loan,
                    get_object=lambda i: i.cognates[0].cognateset,
                    sTitle='loan?', sTooltip='is cognate set marked as loan event'),
                BoolCol(self, 'parallel_loan_event', model_col=CognateClass.parallel_loan_event,
                    get_object=lambda i: i.cognates[0].cognateset,
                    sTitle='pll loan?', sTooltip='is cognate set marked as parallel loan event'),
                DetailsSourceRowLinkCol(self, 'source', button_text='source', sTitle='Source')
            ]
        return [
                CoblFormSelectMeaningCol(self, 'name', model_col=Meaning.name,
                    get_object=lambda i: i.valueset.parameter,
                    select='multiple',
                    choices=get_distinct_values(Meaning.name),
                    sTitle='Meaning',
                    sTooltip='Choose one or more meanings (CTRL/⌘ + click)'),
                CoblFormSelectCladeNameCol(
                    self,
                    'clade_name',
                    model_col=Variety.clade_name,
                    get_object=lambda i: i.valueset.language,
                    select='multiple',
                    sTitle='Clade',
                    sTooltip='Choose one or more clade names (CTRL/⌘ + click)',
                    choices=get_distinct_values(Variety.clade_name)),
                CoblFormSelectLanguageCol(
                    self,
                    'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language,
                    select='multiple',
                    input_size='large',
                    sTooltip='Choose one or more languages (CTRL/⌘ + click)',
                    choices=get_distinct_values(Language.name)),
                LinkCol(self, 'name', sTitle='Lexeme'),
                Col(self, 'native_script', model_col=Lexeme.native_script),
                CognatesetColorCol(self, 'cognate_class', sTitle='Cognate set'),
                BoolCol(self, 'is_loan', model_col=CognateClass.is_loan,
                    get_object=lambda i: i.cognates[0].cognateset,
                    sTitle='loan?', sTooltip='is cognate set marked as loan event'),
                BoolCol(self, 'parallel_loan_event', model_col=CognateClass.parallel_loan_event,
                    get_object=lambda i: i.cognates[0].cognateset,
                    sTitle='pll loan?', sTooltip='is cognate set marked as parallel loan event'),
        ]


class DetailsSourceRowLinkCol(DetailsRowLinkCol):

    def format(self, item):
        if item.valueset.references:
            return button(
                self.button_text,
                href=self.dt.req.resource_url(self.get_obj(item), ext='snippet.html'),
                title="show source",
                class_="btn-info details",
                tag=HTML.button)
        return ''

class BoolCol(Col):
    def format(self, item):
        v = str(self.get_value(item))
        if v == 'True':
            return '<span style="display:block; text-align:center; margin:0 auto;">✓</span>'
        return ''


class CoblSources(Sources):
    def get_default_options(self):
        opts = super(Sources, self).get_default_options()
        opts['aaSorting'] = [[1, 'asc'], [3, 'asc']]
        return opts



class CoblContributors(Contributors):
    def col_defs(self):
        return [
            CoblAuthorNameCol(self, 'name'),
            ContributionsCol(self, 'Contributions', sTitle='Data set'),
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
    config.register_datatable('sources', CoblSources)
    config.register_datatable('clades', CoblClades)
