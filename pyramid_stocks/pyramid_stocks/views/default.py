from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED


@view_config(
    route_name='home',
    renderer='../templates/base.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def my_view(request):
    """ Route back to homepage """
    return {}
