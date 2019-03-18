from clld.web.datatables.base import DetailsRowLinkCol, IdCol, RefsCol, Col, LinkCol, LinkToMapCol
from clld.web.datatables import value, Languages
from clld.db.models.common import Language, Value
from clld.db.util import icontains
from clld_cognacy_plugin.datatables import Meanings, Cognatesets
from clld_cognacy_plugin.models import Cognate, Cognateset

from cobl2.models import CognateClass, Meaning, Variety

class CoblMeanings(Meanings):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'more'),
        ] + Meanings.col_defs(self) + [
            Col(self,
                'count_languages',
                sTitle='# langs',
                model_col=Meaning.count_languages),
            Col(self,
                'count_cognateclasses',
                sTitle='# cognate classes',
                model_col=Meaning.count_cognateclasses),
        ]


class CoblMeaningCol(LinkCol):
    def order(self):
        return [Meaning.name, CognateClass.root_language, CognateClass.root_form]

    def search(self, qs):
        return icontains(Meaning.name, qs)


class CoblLanguages(Languages):
    def get_options(self):
        opts = super(Languages, self).get_options()
        # default sort order on clade name first then on language name
        opts['aaSorting'] = [[1, 'asc'], [2, 'asc']]
        return opts

    def col_defs(self):
        return [
            IdCol(self, 'id', bSortable=False),
            CoblCladeCol(self, 'Clade', model_col=Variety.clade),
            CoblLgNameLinkCol(self, 'name'),
            LinkToMapCol(self, 'm'),
            Col(self, 'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self, 'longitude',
                sDescription='<small>The geographic longitude</small>'),
        ]


class CoblLgNameLinkCol(LinkCol):
    def format(self, item):
        # add to link the historical info as superscript dagger if given
        hist = '<sup title="historical">†</sup>' if item.historical else ''
        obj = super(CoblLgNameLinkCol, self).format(item)
        return '%s%s' % (obj, hist) if obj else ''


class CoblCladeCol(Col):
    def format(self, item):
        # add to clade name the color code as left border
        return '<span style="border-left:12px solid %s;padding-left:5px">%s</span>' % (
            item.color, item.clade)


class CognateClasses(Cognatesets):
    def base_query(self, query):
        return query.outerjoin(Meaning)

    def col_defs(self):
        return [
            IdCol(self, 'ID', model_col=Cognateset.id),
            CoblMeaningCol(self, 'name',
                get_object=lambda cc: cc.meaning_rel,
                sTitle='Meaning'),
            Col(self, 'Root_form', model_col=CognateClass.root_form),
            Col(self, 'Root_gloss', model_col=CognateClass.root_gloss),
            Col(self, 'Root_language', model_col=CognateClass.root_language),
            Col(self, 'Loan_source', model_col=CognateClass.loan_source_languoid),
            LinkCol(
                self,
                'loaned_from',
                sClass='left',
                model_col=CognateClass.loan_source_pk,
                get_object=lambda cc: cc.loan_source),
            RefsCol(self, 'Source'),
        ]


class CognatesetCol(LinkCol):
    __kw__ = dict(bSearchable=False)

    def order(self):
        return Cognate.cognateset_pk

    def get_obj(self, item):
        return item.cognates[0].cognateset


class Forms(value.Values):
    def base_query(self, query):
        query = value.Values.base_query(self, query)
        return query.join(Value.cognates)

    def col_defs(self):
        if self.parameter:
            return [
                LinkCol(
                    self,
                    'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
                Col(self, 'name', sTitle='Lexeme'),
                CognatesetCol(self, 'cognate_class'),
                value.RefsCol(self, 'source'),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
            ]
        if self.language:
            return [
                Col(self, 'name', sTitle='Lexeme'),
                CognatesetCol(self, 'cognate_class'),
                value.RefsCol(self, 'source'),
            ]
        return value.Values.col_defs(self)


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
