from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from sqlalchemy.exc import DBAPIError, IntegrityError
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest, HTTPUnauthorized, HTTPConflict
from . import DB_ERR_MSG
from ..models import Account


@view_config(
    route_name='auth',
    renderer='../templates/login.jinja2',
    permission=NO_PERMISSION_REQUIRED)
def register_page(request):
    """ Open register page """
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']

        except KeyError:
            return {}

        is_authenticated = Account.check_credentials(request, username,
                                                     password)
        if is_authenticated[0]:
            headers = remember(request, userid=username)
            return HTTPFound(location=request.route_url('portfolio'),
                             headers=headers)
        else:
            return HTTPUnauthorized()

    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

        except KeyError:
            return HTTPBadRequest()

        try:
            instance = Account(
                username=username,
                email=email,
                password=password,
            )
            # import pdb; pdb.set_trace()
            headers = remember(request, userid=instance.username)
            request.dbsession.add(instance)

            return HTTPFound(location=request.route_url('portfolio'),
                             headers=headers)

        except DBAPIError:
            return Response(DB_ERR_MSG, content_type='text/plain', status=500)

    return HTTPFound(location=request.route_url('home'))


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)
