from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/index.jinja2')
def my_view(request):
    """ Route back to homepage """
    return {}


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
    return {}


@view_config(route_name='detail', renderer='../templates/stock_detail.jinja2',
             request_method='GET')
def get_detail_view(request):
    """ detail about a user's existing stock """
    return {}