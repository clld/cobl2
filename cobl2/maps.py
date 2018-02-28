from clld.web.maps import ParameterMap, Map


class MeaningMap(ParameterMap):
    def get_options(self):
        return {
            'base_layer': 'Esri.WorldPhysical',
            'icon_size': 15,
        }


class LanguagesMap(Map):
    def get_options(self):
        return {
            'base_layer': 'Esri.WorldPhysical',
            'icon_size': 15,
        }


def includeme(config):
    config.register_map('parameter', MeaningMap)
    config.register_map('languages', LanguagesMap)
