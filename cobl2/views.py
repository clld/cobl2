from pyramid.view import view_config


@view_config(route_name='test')
def test(req):
    from clld.db.models.common import Parameter
    print(list(Parameter.__subclasses__()))
    return {}
