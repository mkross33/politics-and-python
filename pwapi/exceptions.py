"""Custom exceptions for pwapi"""


class APIKeyError(Exception):
    """Base exception for all PW API key errors"""


class KeyLimited(APIKeyError):
    """Raised when API has used up its daily rate limit"""


class InvalidKey(APIKeyError):
    """Raised on use of an invalid API key"""


class InvalidPermissions(APIKeyError):
    """Raised when key used did not have permissions for the endpoint"""


class InvalidRequest(Exception):
    """Raised on invalid API calls"""
