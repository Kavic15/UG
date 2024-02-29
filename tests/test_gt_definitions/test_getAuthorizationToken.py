import pytest
from gql_ug.utils.Dataloaders import getAuthorizationToken

class MockInfo:
    def __init__(self, context):
        self.context = context

def test_getAuthorizationToken_with_request():
    # Mock a request object
    mock_request = {'some_key': 'some_value'}

    # Create a MockInfo object with a context containing the mock request
    mock_info = MockInfo(context={'request': mock_request})

    # Call the function and check if it returns without raising an AssertionError
    getAuthorizationToken(mock_info)

def test_getAuthorizationToken_without_request():
 # Create a MockInfo object with a None context
    mock_info = MockInfo(context=None)

    # Check if the function has a __wrapped__ attribute (if it's wrapped with @cache)
    original_function = getAuthorizationToken

    try:
        # Call the function and check if it raises an AttributeError
        original_function(mock_info)
    except AttributeError as e:
        # Check if the AttributeError is the expected one
        assert "NoneType' object has no attribute 'get" in str(e)
    else:
        pytest.fail("Expected AttributeError, but it was not raised")