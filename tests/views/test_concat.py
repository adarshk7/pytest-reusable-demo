import pytest


class ConcatEndpointTestCase:
    def _get_base_params(self):
        return {
            'value_string': 'Hello',
            'value_integer': 3,
        }

    @pytest.fixture
    def url(self):
        return '/concat'

    @pytest.fixture
    def auth_token(self):
        return 'valid-token'

    @pytest.fixture
    def headers(self, auth_token):
        return {
            'Accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

    @pytest.fixture
    def params(self):
        return self._get_base_params()

    @pytest.fixture
    def response(self, client, url, headers, params):
        return client.get(url, headers=headers, params=params)

    @pytest.fixture
    def expected_status_code(self):
        return 200

    @pytest.fixture
    def expected_response_data(self):
        return {'data': 'Hello and 3'}

    def test_response(self, response, expected_status_code, expected_response_data):
        assert response.status_code == expected_status_code
        assert response.json() == expected_response_data


class TestConcatEndpointResponseSuccessful(ConcatEndpointTestCase):
    pass


class TestConcatEndpointResponseSuccessfulWhenNoStringEmpty(ConcatEndpointTestCase):
    @pytest.fixture
    def params(self):
        _params = self._get_base_params()
        _params['value_string_optional'] = 'Something'
        return _params
    
    @pytest.fixture
    def expected_response_data(self):
        return {'data': 'Hello and 3'}


class TestConcatEndpointUnauthorized(ConcatEndpointTestCase):
    @pytest.fixture
    def expected_status_code(self):
        return 401
    
    @pytest.fixture
    def expected_response_data(self):
        return {'detail': 'Invalid token'}
    
    @pytest.fixture
    def auth_token(self):
        return 'invalid-token'


@pytest.mark.parametrize(('field', 'value', 'error', 'error_type'), [
    ('value_integer', None, 'field required', 'value_error.missing'),
    ('value_integer', 10.11, 'value is not a valid integer', 'type_error.integer'),
    ('value_integer', 'garbage', 'value is not a valid integer', 'type_error.integer'),
    ('value_string', None, 'field required', 'value_error.missing'),
])
class TestConcatEndpointBadRequest(ConcatEndpointTestCase):
    @pytest.fixture
    def params(self, field, value, error, error_type):
        _params = self._get_base_params()
        _params[field] = value
        return _params

    @pytest.fixture
    def expected_status_code(self):
        return 422

    @pytest.fixture
    def expected_response_data(self, field, value, error, error_type):
        return {'detail': [{'loc': ['query', field], 'msg': error, 'type': error_type}]}
