# from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests


@view_config(route_name='home', renderer='../templates/base.jinja2')
def my_view(request):
    """ Route back to homepage """
    return {}


@view_config(route_name='auth', renderer='../templates/register.jinja2')
def register_page(request):
    """ Open register page """
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            print('User: {}, Pass: {}, Email: {}'.format(
                                                username, password, email))
            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return HTTPNotFound()

    return HTTPNotFound()


@view_config(route_name='stock', renderer='../templates/stock_add.jinja2')
def searching_stock_ticker(request):
    """ searching for a stock ticker symbol """
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}
        address = 'https://api.iextrading.com/1.0/\
stock/{}/company'.format(symbol)
        response = requests.get(address)
        response = response.json()

        return {'entry': response}

    elif request.method == 'POST':
        symbol = request.POST['new_stock']
        symbol = symbol.lower()
        for entries in MOCK_DATA:
            for val in entries.values():
                # import pdb; pdb.set_trace()
                if val == symbol.upper():
                    return HTTPFound(location=request.route_url('portfolio'))

        address = 'https://api.iextrading.com/1.0/stock/{}/company'.format(symbol)
        response = requests.get(address)
        response = response.json()
        MOCK_DATA.append(
            {'symbol': response['symbol'],
                'companyName': response['companyName'],
                'exchange': response['exchange'],
                'industry': response['industry'],
                'website': response['website'],
                'description': response['description'],
                'CEO': response['CEO'],
                'issueType': response['issueType'],
                'sector': response['sector']})
        return HTTPFound(location=request.route_url('portfolio'))
    else:
        return HTTPNotFound()


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
