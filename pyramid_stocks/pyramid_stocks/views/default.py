from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/base.jinja2')
def my_view(request):
    """ Route back to homepage """
    return {}
