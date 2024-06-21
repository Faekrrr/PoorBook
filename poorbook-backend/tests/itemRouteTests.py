import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app import app  
from data.itemRepository import ItemRepository 
from common.config import Config


#Config
client = TestClient(app)
config = Config()
API_KEY = config.API_KEY

#Base API URL
API_URL = '/api/v1'

#Auth header
API_HEADER = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
        }

#Fake data
API_MOCK_DATA = [
        {"id": "1", 
         "name": "Item 1", 
         "description": "Description 1", 
         "location": "Location 1", 
         "locationDetails": "Details 1", 
         "quantity": 10},
        
        {"id": "2", 
         "name": "Item 2", 
         "description": "Description 2", 
         "location": "Location 2", 
         "locationDetails": "Details 2", 
         "quantity": 20},
    ]

#Fake new item
API_TEST_ITEM = {
        "name": "Test Item",
        "description": "This is a test item",
        "location": "Test Location",
        "locationDetails": "Test Location Details",
        "quantity": 5
    }


@pytest.fixture
def getMockedRepository():
    """ Get new MagicMocn instance. """
    return MagicMock(spec=ItemRepository)


def test_createNewItem_ShouldReturn201(getMockedRepository):
    """ POST /items test should return 201 and created Id. """
    app.dependency_overrides[ItemRepository] = lambda: getMockedRepository
        
    response = client.post(
        f"{API_URL}/items",  
        json=API_TEST_ITEM,
        headers=API_HEADER
    )
    
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["content"]["result"]["id"] == "123"

    app.dependency_overrides = {}
    
    
def test_createNewItem_ShouldReturn422(getMockedRepository):
    """ POST /items test should return 422 status code. """
    app.dependency_overrides[ItemRepository] = lambda: getMockedRepository
    
    newItem = {
        "name": "Test Item",
        "description": "This is a test item",
        "location": "Test Location",
        "locationDetails": "Test Location Details",
        "quantity": "test"
    }
    
    response = client.post(
        f"{API_URL}/items",  
        json=newItem,
        headers=API_HEADER
    )
    
    assert response.status_code == 422

    app.dependency_overrides = {}


def test_getAllItems_shouldReturnContent(getMockedRepository):
    """ GET /items test should return 201 and content. """
    getMockedRepository.getSorted.return_value = API_MOCK_DATA
    
    app.dependency_overrides[ItemRepository] = lambda: getMockedRepository
    
    
    response = client.get(
        f"{API_URL}/items?offset=0&take=10&order=ASC&sortBy=created",  
        headers=API_HEADER
    )
    
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["statusCode"] == 200
    assert response_json["content"]["result"][0]["id"] == "1"
    assert response_json["content"]["result"][1]["id"] == "2"
    
    app.dependency_overrides = {}


def test_deleteItem_ShouldReturn204(getMockedRepository):
    """ DELETE /tasks test should return 204 status code. """
    getMockedRepository.getSorted.return_value = API_MOCK_DATA
    
    app.dependency_overrides[ItemRepository] = lambda: getMockedRepository
    
    response = client.delete(
        f"{API_URL}/items/1",  
        headers=API_HEADER
    )
    
    assert response.status_code == 204
    
    app.dependency_overrides = {}
    

def test_updateItem_ShouldReturn204(getMockedRepository):
    """ PUT /items test should return 204 status code. """
    app.dependency_overrides[ItemRepository] = lambda: getMockedRepository
    
    changes_payload = {
        "name": "Updated Item Name",
        "description": "Updated item description",
        "location": "Updated Location",
        "locationDetails": "Updated Location Details"
    }
    
    response = client.put(f"{API_URL}/items/test_id", 
                          json=changes_payload, 
                          headers=API_HEADER)
    
    assert response.status_code == 204

    app.dependency_overrides = {}
     