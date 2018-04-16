from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from sqlalchemy.exc import DBAPIError, IntegrityError
from . import DB_ERR_MSG
from ..models import Stock
from ..models import Account
from ..sample_data import MOCK_DATA
import requests


@view_config(
    route_name='home',
    renderer='../templates/base.jinja2',
    request_method='GET',
    permission=NO_PERMISSION_REQUIRED)
def my_view(request):
    """ Route back to homepage """
    return {}


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
        if response._content.decode('utf8') == 'Unknown symbol':
            return {}
        response = response.json()

        return {'entry': response}

    if request.method == 'POST':
        try:
            symbol = request.POST['new_stock']
        except KeyError:
            raise HTTPBadRequest()

        try:
            address = 'https://api.iextrading.com/1.0/\
stock/{}/company'.format(symbol)
            response = requests.get(address)
            data = response.json()

        except ValueError:
            return HTTPNotFound()

        query = request.dbsession.query(Account)
        instance = query.filter(Account.username == request.authenticated_userid).first()

        query = request.dbsession.query(Stock)
        instance2 = query.filter(Stock.symbol == request.POST['new_stock']).first()

        if instance2:
            instance2.account_id.append(instance)

        else:
            new = Stock(**data)
            # instance = Stock(**data)

        try:
            new = Stock(**data)
            request.dbsession.add(new)
            request.dbsession.flush()

        except IntegrityError:
            pass

    return HTTPFound(location=request.route_url('portfolio'))


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2',
             request_method='GET')
def view_existing_stocks(request):
    """ display user's existing stocks"""

    query = request.dbsession.query(Stock)
    all_entries = query.all()
    return {'entries': all_entries}


@view_config(route_name='detail', renderer='../templates/stock_detail.jinja2',
             request_method='GET')
def get_detail_view(request):
    """ detail about a user's existing stock """
    try:
        symbol = request.matchdict['symbol']
    except KeyError:
        return HTTPNotFound()

    try:
        query = request.dbsession.query(Stock)

    except DBAPIError:
        return DBAPIError(DB_ERR_MSG, content_type='text/plain', status=500)

    for entry in query.all():
        if entry.symbol == symbol:
            return {'result': entry}

    return HTTPNotFound
