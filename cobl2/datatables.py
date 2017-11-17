from clld.web.datatables.base import DetailsRowLinkCol
from clld_cognacy_plugin.datatables import Meanings


class CoblMeanings(Meanings):
    def col_defs(self):
        return [DetailsRowLinkCol(self, 'more')] + Meanings.col_defs(self)


def includeme(config):
    config.register_datatable('parameters', CoblMeanings)
