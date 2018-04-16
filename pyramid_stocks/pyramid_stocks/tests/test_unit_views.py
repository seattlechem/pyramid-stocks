def test_default_behavior_of_base_route(dummy_request):
    from ..views.default import my_view

    request = dummy_request
    response = my_view(request)
    assert isinstance(response, dict)
    assert response == {}


def test_default_behavior_of_auth_route(dummy_request):
    from ..views.auth import register_page
    request = dummy_request
    response = register_page(request)
    assert response == {}
