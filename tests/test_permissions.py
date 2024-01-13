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