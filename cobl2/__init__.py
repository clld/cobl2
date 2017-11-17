from clld.interfaces import IContribution, ILinkAttrs
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


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    #config.include('clld_glottologfamily_plugin')
    config.include('clld_cognacy_plugin')
    config.add_route('test', '/test')
    config.registry.registerUtility(link_attrs, ILinkAttrs)
    return config.make_wsgi_app()
