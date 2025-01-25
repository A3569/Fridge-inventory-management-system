import requests

# Base URL for API endpoints
API_BASE_URL = 'http://127.0.0.1:8000'  # Remove /api/v1 from base URL

# Define all API endpoints
API_ENDPOINTS = {
    'addToInventory': f'{API_BASE_URL}/user/api/v1/addToInventory',
    'removeFromInventory': f'{API_BASE_URL}/user/api/v1/removeFromInventory',
    'addToShoppingList': f'{API_BASE_URL}/user/api/v1/addToShoppingList',
    'removeFromShoppingList': f'{API_BASE_URL}/user/api/v1/removeFromShoppingList',
    'purchaseItem': f'{API_BASE_URL}/user/api/v1/purchaseItem',
}

class APIConfig:
    # Base URL for API server
    BASE_URL = 'http://localhost:3000/api/v1'
    
    @staticmethod
    def make_request(method, endpoint, data=None):
        url = f"{API_BASE_URL}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return None 