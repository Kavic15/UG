'''
import pytest
from httpx import AsyncClient
from main import app  # Assuming your FastAPI app is named 'app'

@pytest.mark.asyncio
async def test_permissions():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # Step 1: Perform a query/mutation that requires authentication
        query = """
        query {
            rbac_by_id(id: "your_test_id") {
                id
                asUser
                asGroup
            }
        }
        """
        response = await client.post("/graphql", json={"query": query})
        
        # Step 2: Check that the response indicates the need for authentication
        assert response.status_code == 200
        assert "User is not authenticated" in response.text

        # Step 3: If needed, perform authentication (e.g., login) and get an access token

        # Step 4: Retry the query/mutation with authentication headers
        authenticated_response = await client.post(
            "/graphql",
            json={"query": query},
            headers={"Authorization": "Bearer your_access_token"},
        )

        # Step 5: Check that the authenticated response is successful
        assert authenticated_response.status_code == 200
        assert "data" in authenticated_response.json()

        # Step 6: Add more tests for specific permission scenarios as needed
        # For example, test a query/mutation that requires a specific role or permission

        # Step 7: Repeat the process for other scenarios or permissions

# Run the test using: pytest -k test_permissions
'''
import pytest
from unittest.mock import Mock
from strawberry import Schema
from GraphTypeDefinitions.RBACObjectGQLModel import RBACObjectGQLModel
from GraphPermissions import OnlyForAuthentized, UserGDPRPermission, UserEditorPermission, GroupEditorPermission

@pytest.mark.asyncio
async def test_rbac_object_permissions():
    schema = Schema(query=RBACObjectGQLModel)

    # Mock the resolver info
    info = Mock()

    # Example: Mocking a user with specific permissions
    user_with_permissions = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "roles": [
            {
                "valid": True,
                "group": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                    "name": "Uni"
                },
                "roletype": {
                    "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                    "name": "administrátor"
                }
            }
        ]
    }
    
    # Set the user context in the info
    info.context = {"user": user_with_permissions}

    # Test RBACObjectGQLModel with OnlyForAuthentized permission
    result = await schema.execute("query { rbac_by_id(id: \"2d9dc5ca-a4a2-11ed-b9df-0242ac120003\") { id } }", info=info)
    assert result.errors is None

    # Example: Test RBACObjectGQLModel with GroupEditorPermission
    info.context["session"] = Mock()  # Mock the session for the permission check
    result = await schema.execute("query { rbac_by_id(id: \"2d9dc5ca-a4a2-11ed-b9df-0242ac120003\") { id } }", info=info)
    assert result.errors is None

    # Example: Test RBACObjectGQLModel with UserGDPRPermission
    result = await schema.execute("query { rbac_by_id(id: \"2d9dc5ca-a4a2-11ed-b9df-0242ac120003\") { id } }", info=info)
    assert result.errors is None


@pytest.mark.asyncio
async def test_group_editor_permission():
    schema = Schema(query=GroupEditorPermission)

    # Mock the resolver info
    info = Mock()

    # Example: Mocking a user with specific permissions
    user_with_permissions = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "roles": [
            {
                "valid": True,
                "group": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                    "name": "Uni"
                },
                "roletype": {
                    "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                    "name": "administrátor"
                }
            }
        ]
    }
    
    # Set the user context in the info
    info.context = {"user": user_with_permissions, "session": Mock()}

    # Test GroupEditorPermission
    result = await schema.execute("query { has_permission }", info=info)
    assert result.errors is None


@pytest.mark.asyncio
async def test_user_gdpr_permission():
    schema = Schema(query=UserGDPRPermission)

    # Mock the resolver info
    info = Mock()

    # Example: Mocking a user with specific permissions
    user_with_permissions = {
        "id": "2d9dc5ca-a4a2-11ed-b9df-0242ac120003",
        "roles": [
            {
                "valid": True,
                "group": {
                    "id": "2d9dcd22-a4a2-11ed-b9df-0242ac120003",
                    "name": "Uni"
                },
                "roletype": {
                    "id": "ced46aa4-3217-4fc1-b79d-f6be7d21c6b6",
                    "name": "administrátor"
                }
            }
        ]
    }
    
    # Set the user context in the info
    info.context = {"user": user_with_permissions, "session": Mock()}

    # Test UserGDPRPermission
    result = await schema.execute("query { has_permission }", info=info)
    assert result.errors is None