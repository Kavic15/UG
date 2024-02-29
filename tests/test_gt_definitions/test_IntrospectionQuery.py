import requests
import pytest
import os

introspection_query = """
  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        args {
          ...InputValue
        }
      }
    }
  }

  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }

  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }

  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
        }
      }
    }
  }
"""

def test_save_introspection_query():
    graphql_endpoint = 'http://localhost:8000/gql'
    filename = 'IntrospectionQuery.txt'
    
    # Make the GraphQL introspection query
    response = requests.post(graphql_endpoint, json={'query': introspection_query})

    # Check if the request was successful (status code 200) && check if the file exists
    assert response.status_code == 200, f"Failed to execute introspection query. Status code: {response.status_code}"
    assert os.path.isfile(filename), f"File {filename} is not accessible."
    # Save the introspection query result into a txt file
    with open('IntrospectionQuery.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)