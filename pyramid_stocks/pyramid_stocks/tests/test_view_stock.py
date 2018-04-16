# Default view properties
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.security import remember


def test_default_response_portfolio_view(dummy_request):
    from ..views.default import view_existing_stocks

    response = view_existing_stocks(dummy_request)
    assert isinstance(response, dict)
    assert response['entries'] == []


def test_default_get_portfolio_detail_view(dummy_request, db_session, test_stock):
    from ..views.default import get_detail_view

    db_session.add(test_stock)

    dummy_request.matchdict = {'symbol': 'fake'}
    response = get_detail_view(dummy_request)
    assert type(response) == dict
    assert response['result'].symbol == 'fake'


def test_detail_not_found(dummy_request):
        from ..views.default import get_detail_view
        from pyramid.httpexceptions import HTTPNotFound

        response = get_detail_view(dummy_request)
        assert isinstance(response, HTTPNotFound)


def test_default_response_get_stock_view(dummy_request):
    from ..views.default import searching_stock_ticker

    response = searching_stock_ticker(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_valid_post_to_get_stock_view(dummy_request):
    from ..views.default import searching_stock_ticker
    from pyramid.httpexceptions import HTTPFound

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "new_stock": "FB",
        }

    response = searching_stock_ticker(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_valid_post_to_get_stock_view_adds_record_to_db(dummy_request, test_account, db_session):
    from ..views.default import searching_stock_ticker
    from ..models import Stock

    db_session.add(test_account)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "new_stock": "FB",
        }

# assert right here that there's nothing in the DB
    searching_stock_ticker(dummy_request)
    query = db_session.query(Stock)
    one = query.first()
    assert one.companyName == 'Facebook Inc.'
    assert one.symbol == 'FB'
    assert type(one.id) == int


def test_invalid_post_to_get_stock_view(dummy_request):
    import pytest
    from ..views.default import searching_stock_ticker

    dummy_request.method = 'POST'
    dummy_request.POST = {}

    with pytest.raises(HTTPBadRequest):
        # import pdb; pdb.set_trace()
        response = searching_stock_ticker(dummy_request)
        assert isinstance(response, HTTPBadRequest)
