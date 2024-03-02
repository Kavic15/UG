import os
import pytest
import sqlalchemy
from gql_ug.DBDefinitions import ComposeConnectionString
from gql_ug.utils.Dataloaders import composeAuthUrl


from gql_ug.DBDefinitions import startEngine

import sqlalchemy.exc



@pytest.mark.asyncio
async def test_startEngine_with_makeDrop_and_makeUp():
    connection_string = ComposeConnectionString()
    async_session_maker = await startEngine(connectionstring=connection_string, makeDrop=True, makeUp=True)
    assert async_session_maker is not None

@pytest.mark.asyncio
async def test_startEngine_with_makeDrop_False_and_makeUp_True():
    connection_string = ComposeConnectionString()
    async_session_maker = await startEngine(connectionstring=connection_string, makeDrop=False, makeUp=True)
    assert async_session_maker is not None

# @pytest.mark.asyncio #NNNNNN
# async def test_startEngine_with_makeDrop_True_and_makeUp_False():
#     connection_string = ComposeConnectionString()
#     async_session_maker = await startEngine(connectionstring=connection_string, makeDrop=True, makeUp=False)
#     print()
#     print()
#     print(f"async_session_maker: {async_session_maker}")
#     assert async_session_maker is None

# @pytest.mark.asyncio #NNNNNN
# async def test_startEngine_with_makeDrop_and_makeUp_False():
#     connection_string = ComposeConnectionString()
#     async_session_maker = await startEngine(connectionstring=connection_string, makeDrop=False, makeUp=False)
#     assert async_session_maker is None




def test_ComposeConnectionString():
    os.environ["POSTGRES_USER"] = "test_user"
    os.environ["POSTGRES_PASSWORD"] = "test_password"
    os.environ["POSTGRES_DB"] = "test_db"
    os.environ["POSTGRES_HOST"] = "test_host:5432"

    # Get connection string
    connection_string = ComposeConnectionString()

   
    expected_connection_string = "postgresql+asyncpg://test_user:test_password@test_host:5432/test_db"
    assert connection_string == expected_connection_string
    #delete variables
    del os.environ["POSTGRES_USER"]
    del os.environ["POSTGRES_PASSWORD"]
    del os.environ["POSTGRES_DB"]
    del os.environ["POSTGRES_HOST"]



def test_composeAuthUrl_valid_url():
    os.environ["AUTHURL"] = "http://localhost:8088/gql"
    assert composeAuthUrl() == "http://localhost:8088/gql"
    del os.environ["AUTHURL"]

def test_composeAuthUrl_invalid_url_missing_protocol():
    os.environ["AUTHURL"] = "localhost:8088/gql"

    # Check if the function has a __wrapped__ attribute (if it's wrapped with @cache)
    if hasattr(composeAuthUrl, '__wrapped__'):
        original_function = composeAuthUrl.__wrapped__
    else:
        original_function = composeAuthUrl

    with pytest.raises(AssertionError, match="probably bad formated url, has it 'protocol' part?"):
        original_function()

    del os.environ["AUTHURL"]

def test_composeAuthUrl_invalid_url_invalid_hostname():
    os.environ["AUTHURL"] = "http://invalid.hostname"

    # Check if the function has a __wrapped__ attribute (if it's wrapped with @cache)
    if hasattr(composeAuthUrl, '__wrapped__'):
        original_function = composeAuthUrl.__wrapped__
    else:
        original_function = composeAuthUrl

    with pytest.raises(AssertionError, match="security check failed, change source code"):
        original_function()

    del os.environ["AUTHURL"]