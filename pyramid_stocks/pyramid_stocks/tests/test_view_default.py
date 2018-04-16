# Default view properties


def test_default_response_my_view(dummy_request):
    from ..views.default import my_view

    response = my_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# Auth View Functionality
def test_default_response_register_page(dummy_request):
    from ..views.auth import register_page

    response = register_page(dummy_request)
    assert response == {}


def test_auth_signin_view(dummy_request):
    from ..views.auth import register_page

    dummy_request.GET = {'username': 'watman', 'password': 'whodat'}
    response = register_page(dummy_request)
    assert response.status_code == 401


def test_auth_signup_view(dummy_request):
    from ..views.auth import register_page
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'watman', 'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = register_page(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_signup_view(dummy_request):
    from ..views.auth import register_page
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = register_page(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    from ..views.auth import register_page
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = register_page(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_default_notfound(dummy_request):
    from ..views.notfound import notfound_view

    assert notfound_view(dummy_request) == {}


def test_default_logout(dummy_request):
    from ..views.auth import logout
    from pyramid.httpexceptions import HTTPFound

    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)
