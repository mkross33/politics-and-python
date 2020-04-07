""" Functions that make http requests to the PW servers"""
import requests
import json
from pwapi.exceptions import *


def call_api(url: str) -> dict:
    """Calls a given PW API endpoint"""

    r = requests.get(url)
    if not r.ok:
        r.raise_for_status()
    try:
        data = r.json()
    except json.JSONDecodeError:
        fixed = fix_json(r.text)
        data = json.loads(fixed)
    validate_api_data(data)
    return data


def fix_json(text: str) -> str:
    """Fixes malformed JSON

    :param text: JSON string
    :return a fixed JSON string"""

    attempts = 5
    current_error = ""
    fixed = False
    while not fixed:
        if attempts == 0:
            raise RuntimeError(f"Couldn't fix bad JSON. Last error was: {current_error}")
        attempts -= 1
        try:
            json.loads(text)
            fixed = True
        except json.JSONDecodeError as e:
            current_error = e
            if e.msg == "Extra data":
                # The extra data is always irrelevant to the API call and sliced off
                text = text[:e.pos]
            # Caused by some APIs separating properties with double commas
            elif e.msg == "Expecting property name enclosed in double quotes":
                text = text.replace(",,", ",")
            else:
                raise RuntimeError(f"Unexpected error in returned JSON: {e}")
    return text


def validate_api_data(data: dict) -> None:
    """Validates data, raising matching exceptions for any API error messages"""

    errors = {"Invalid API key.": InvalidKey("Invalid API Key."),
              "Exceeded max request limit of 2000 for today.": KeyLimited("Exceeded daily call limit."),
              "Exceeded max request limit of 5000 for today.": KeyLimited("Exceeded daily call limit."),
              # technically this shouldn't crop up as all call functions require a key, but its here for consistency
              "No API key was provided.": InvalidKey("No API key was provided."),
              "War does not exist.": InvalidRequest("War does not exist."),
              "Alliance does not exist.": InvalidRequest("Alliance does not exist."),
              "Nation doesn't exist.": InvalidRequest("Nation does not exist."),
              "Alliance doesn't exist.": InvalidRequest("Alliance does not exist."),
              "City doesn't exist.": InvalidRequest("City does not exist.")
              }

    # Most endpoints key errors to general_message, a few to error
    if "general_message" in data:
        raise errors[data["general_message"]]
    elif "error" in data:
        raise errors[data["error"]]
    else:
        return
