import os
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy


def includeme(config):
    pass
