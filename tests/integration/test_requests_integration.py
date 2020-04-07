import requests
import requests_mock
import pytest
import os
from pwapi.requests import call_api
from pwapi.exceptions import *

key = os.getenv("PW_KEY")

class TestCallAPI:
    def test_bad_end_point_raises_error(self):
        with pytest.raises(requests.exceptions.HTTPError):
            call_api("http://politicsandwar.com/api/badendpoint")

    def test_fixes_json(self):
        # request is mocked while testing that the fix json functions are properly called. Malformed JSON is returned
        # randomly, I know of no way to guarantee its delivery in a real API call.
        with requests_mock.Mocker() as m:
            m.get('http://doublecomma', text='{"key1": "val",, "key2": "val"}>SERVERERROR')
            assert call_api("http://doublecomma") == {"key1": "val", "key2": "val"}

    def test_api_errors_throw_exception(self):
        with pytest.raises(InvalidKey):
            call_api("http://politicsandwar.com/api/alliance-members/?allianceid=615&key=badkey")

        with pytest.raises(InvalidRequest):
            call_api(f"http://politicsandwar.com/api/nation/id=noid&key={key}")

    def test_good_call_returns_data(self):
        # mocked to use a fixed stub of API data, as there is no way to get any real endpoint to always return the same
        # data for consistent testing
        stub = '{"cityids":["52120","52148"],"success":true,"nationid":"31191","name":"Reach"}'
        with requests_mock.Mocker() as m:
            m.get("http://politicsandwar.com/api/natoion/id=31191&key=key", text=stub)
            data = call_api("http://politicsandwar.com/api/natoion/id=31191&key=key")
            assert data == {"cityids": ["52120", "52148"], "success": True, "nationid": "31191", "name": "Reach"}