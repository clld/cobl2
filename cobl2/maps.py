from clld.web.maps import ParameterMap, Map
from clld_cognacy_plugin.maps import CognatesetMap


class MeaningMap(ParameterMap):
    def get_options(self):
        return {
            'icon_size': 15,
            'max_zoom': 8,
        }


class LanguagesMap(Map):
    def get_options(self):
        return {
            'icon_size': 15,
            'max_zoom': 8,
        }


class CoblCognateSetMap(CognatesetMap):
    def get_default_options(self):
        return {
            'info_query': {
                'parameter': self.ctx.pk,
                'is_cognateset_map': True,
            },
            'hash': True}

    def get_options(self):
        return {
            'icon_size': 15,
            'max_zoom': 8,
        }


def includeme(config):
    config.register_map('parameter', MeaningMap)
    config.register_map('languages', LanguagesMap)
