from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound


@view_config(route_name='home', renderer='../templates/base.jinja2')
def my_view(request):
    """ Route back to homepage """
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route.url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User: {}, Pass: {}, Email: {}'.format(
                                             username, password, email))

        return HTTPFound(location=request.route.url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='auth', renderer='../templates/register.jinja2',
             request_method='GET')
def register_page(request):
    """ Open register page """
    return {}


@view_config(route_name='stock', renderer='../templates/stock_add.jinja2',
             request_method='GET')
def searching_stock_ticker(request):
    """ searching for a stock ticker symbol """
    return {}


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2',
             request_method='GET')
def view_existing_stocks(request):
    """ display user's existing stocks"""
    return {'entries': MOCK_DATA}


@view_config(route_name='detail', renderer='../templates/stock_detail.jinja2',
             request_method='GET')
def get_detail_view(request):
    """ detail about a user's existing stock """
    symbol = request.matchdict['symbol']
    for entry in MOCK_DATA:
        if entry['symbol'] == symbol:
            return {'result': entry}
    return {}
