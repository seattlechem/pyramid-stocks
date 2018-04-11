# from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests


@view_config(route_name='home', renderer='../templates/base.jinja2')
def my_view(request):
    """ Route back to homepage """
    return {}
