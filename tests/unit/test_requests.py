import pytest
from pwapi.requests import *


class TestFixJSON:
    def test_fixes_extra_data(self):
        bad_json = '{ "key": "val"}<bad data>'
        fixed = fix_json(bad_json)
        assert fixed == '{ "key": "val"}'

    def test_fixes_double_comma(self):
        bad_json = '{"key1": "val",, "key2": "val"}'
        fixed = fix_json(bad_json)
        assert fixed == '{"key1": "val", "key2": "val"}'

    def test_unknown_error_throws_exception(self):
        with pytest.raises(RuntimeError) as e:
            bad_json = '<h1>Header</h1><p>This is HTML, not JSON!</p>'
            fix_json(bad_json)
        assert e.value.args[0] == "Unexpected error in returned JSON: Expecting value: line 1 column 1 (char 0)"

    def test_loop_breaks_with_unfixable_known_error(self):
        with pytest.raises(RuntimeError) as e:
            bad_json = "{'key': 'val'}"
            fix_json(bad_json)
        assert e.value.args[0] == "Couldn't fix bad JSON. Last error was: Expecting property name enclosed in double " \
                                  "quotes: line 1 column 2 (char 1)"


class TestValidateAPIData:
    def test_invalid_key_throws_exception(self):
        with pytest.raises(InvalidKey):
            data = {"general_message": "Invalid API key."}
            validate_api_data(data)

    def test_key_limited_2000_calls_throws_exception(self):
        with pytest.raises(KeyLimited):
            data = {"general_message": "Exceeded max request limit of 2000 for today."}
            validate_api_data(data)

    def test_key_limited_5000_calls_throws_exception(self):
        with pytest.raises(KeyLimited):
            data = {"general_message": "Exceeded max request limit of 5000 for today."}
            validate_api_data(data)

    def test_no_key_throws_exception(self):
        with pytest.raises(InvalidKey):
            data = {"general_message": "No API key was provided."}
            validate_api_data(data)

    def test_no_matching_war(self):
        with pytest.raises(InvalidRequest):
            data = {"general_message": "War does not exist."}
            validate_api_data(data)

    def test_no_matching_alliance(self):
        with pytest.raises(InvalidRequest):
            data = {"general_message": "Alliance does not exist."}
            validate_api_data(data)

    def test_no_matching_nation(self):
        with pytest.raises(InvalidRequest):
            data = {"error": "Nation doesn't exist."}
            validate_api_data(data)

    def test_no_matching_city(self):
        with pytest.raises(InvalidRequest):
            data = {"error": "City doesn't exist."}
            validate_api_data(data)

    def test_no_errors_returns_none(self):
        data = {"nationid": 31191, "leadername": "Mikey"}
        assert validate_api_data(data) is None
