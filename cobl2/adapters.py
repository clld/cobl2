from clld.db.meta import DBSession

from clld_phylogeny_plugin.interfaces import ITree
from clld_phylogeny_plugin.tree import Tree
from clld_phylogeny_plugin.models import Phylogeny


class CognateClassTree(Tree):
    def __init__(self, req, param):
        self._param = param
        Tree.__init__(self, Phylogeny.get('2'), req)

    @property
    def parameters(self):
        return [self._param]

    def get_marker(self, valueset):
        color = '#fff'
        if valueset.values and valueset.values[0].cognates:
            color = valueset.values[0].cognates[0].cognateset.color
        return 'c', color


def includeme(config):
    config.registry.registerUtility(CognateClassTree, ITree)
