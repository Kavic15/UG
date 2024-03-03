import pytest
from gql_ug.utils.Dataloaders import getUgConnection

class MockInfo:
    def __init__(self, context):
        self.context = context

def test_getUgConnection_with_connection():
    # Mock a connection object
    mock_connection = {'some_key': 'some_value'}

    # Create a MockInfo object with a context containing the mock connection
    mock_info = MockInfo(context={'ug_connection': mock_connection})

    # Call the function and check if it returns the expected connection
    result = getUgConnection(mock_info)
    assert result == mock_connection

def test_getUgConnection_without_connection():
    # Create a MockInfo object with a None context
    mock_info = MockInfo(context=None)

    # Call the function and check if it raises an AttributeError
    with pytest.raises(AttributeError):
        getUgConnection(mock_info)