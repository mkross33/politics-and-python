import requests
import requests_mock
import pytest
from pwapi.requests import call_api


class TestCallAPI:
    def test_server_error_raises_exception(self):
        with requests_mock.Mocker() as m:
            m.get('http://politicsandwar.com/api/badendpoint', text="Not Found", status_code=404)
            with pytest.raises(requests.exceptions.HTTPError):
                call_api("http://politicsandwar.com/api/badendpoint")
