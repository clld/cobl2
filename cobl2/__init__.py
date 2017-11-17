from clld.interfaces import IContribution, ILinkAttrs, IValueSet, ILanguage, IMapMarker
from clld.web.icon import MapMarker
from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from cobl2 import models


_ = lambda s: s
_('Contributor')
_('Contributors')
_('Parameter')
_('Parameters')


def link_attrs(req, obj, **kw):
    if IContribution.providedBy(obj):
        # we are about to link to a contribution details page: redirect to language!
        kw['href'] = req.route_url('language', id=obj.variety.id, **kw.pop('url_kw', {}))
    return kw


class CoblMapMarker(MapMarker):
    def __call__(self, ctx, req):
        color = None
        if IValueSet.providedBy(ctx):
            color = ctx.language.color

        if ILanguage.providedBy(ctx):
            color = ctx.color

        if color:
            return req.static_url('cobl2:static/icons/c%s.png' % color)

        return super(CoblMapMarker, self).__call__(ctx, req)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    #config.include('clld_glottologfamily_plugin')
    config.include('clld_cognacy_plugin')
    config.add_route('test', '/test')
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    config.registry.registerUtility(CoblMapMarker(), IMapMarker)
    return config.make_wsgi_app()
