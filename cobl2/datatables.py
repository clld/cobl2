from clld.web.datatables.base import DetailsRowLinkCol, IdCol, RefsCol, Col, LinkCol, LinkToMapCol
from clld.web.datatables import value
from clld.db.models.common import Language, Value
from clld_cognacy_plugin.datatables import Meanings, Cognatesets
from clld_cognacy_plugin.models import Cognate

from cobl2.models import CognateClass


class CoblMeanings(Meanings):
    def col_defs(self):
        return [DetailsRowLinkCol(self, 'more')] + Meanings.col_defs(self)


class CognateClasses(Cognatesets):
    def col_defs(self):
        return [
            IdCol(self, 'ID'),
            Col(self, 'Root form', model_col=CognateClass.root_form),
            Col(self, 'Root gloss', model_col=CognateClass.root_gloss),
            Col(self, 'Root language', model_col=CognateClass.root_language),
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
                value.ValueNameCol(self, 'form'),
                CognatesetCol(self, 'cognate_class'),
                value.RefsCol(self, 'source'),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
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
    config.register_datatable('parameters', CoblMeanings)
