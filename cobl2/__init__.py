from base64 import b64encode

from clld.interfaces import IContribution, ILinkAttrs, IValueSet, ILanguage, IMapMarker, IValue
from clld.web.icon import MapMarker
from clld.web.app import register_menu
from clldutils import svg
from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from cobl2 import models, datatables, interfaces


_ = lambda s: s
_('Value')
_('Values')
_('Contributor')
_('Contributors')
_('Parameter')
_('Parameters')
_('Cognateset')
_('Cognatesets')


def link_attrs(req, obj, **kw):
    if IContribution.providedBy(obj):
        # we are about to link to a contribution details page: redirect to language!
        kw['href'] = req.route_url('language', id=obj.variety.id, **kw.pop('url_kw', {}))
    return kw


class CoblMapMarker(MapMarker):
    def __call__(self, ctx, req):
        color, shape = None, 'c'
        if IValue.providedBy(ctx):
            if ctx.cognates:
                color = ctx.cognates[0].cognateset.color
            else:
                color = '#fff'

        if IValueSet.providedBy(ctx):
            v = ctx.values[0]
            if v.cognates:
                color = v.cognates[0].cognateset.color
            else:
                color = '#fff'
            if ctx.language.historical:
                shape = 'd'

        if ILanguage.providedBy(ctx):
            color = ctx.color
            if ctx.historical:
                shape = 'd'

        if color:
            if color.startswith('#'):
                color = color[1:]
            return svg.data_url(svg.icon(shape + color))

        return super(CoblMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
            'parameters': '/meanings',
            'parameter': '/meaning/{id:[^/\.]+}',
            'values': '/lexemes',
            'value': '/lexeme/{id:[^/\.]+}',
            'language': '/language/{id:[^/\.]+}',
            'cognateset': '/cognateset/{id:[^/\.]+}',
            'source': '/source/{id:[^/\.]+}',
            'contributors': '/authors',
            'contributor': '/author/{id:[^/\.]+}',
        }
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_phylogeny_plugin')
    config.include('clld_cognacy_plugin')
    config.register_datatable('cognatesets', datatables.CognateClasses)
    config.add_route('test', '/test')
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    config.registry.registerUtility(CoblMapMarker(), IMapMarker)
    config.register_resource('clade', models.Clade, interfaces.IClade, True)
    config.register_resource('policie', models.Policie, interfaces.IPolicie, True)
    return config.make_wsgi_app()
