const API_BASE_URL = 'http://127.0.0.1:8000/user/api/v1';  // Update base URL

async function makeAPIRequest(endpoint, method, data = null) {
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            credentials: 'include',
            body: data ? JSON.stringify(data) : null
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'API request failed');
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Common functions for all pages
async function removeFromInventory(itemId) {
    if (confirm('Are you sure you want to remove this item?')) {
        try {
            await makeAPIRequest('removeFromInventory', 'DELETE', { itemId });
            location.reload();
        } catch (error) {
            alert('Failed to remove item');
        }
    }
}

async function addToShoppingList(event) {
    event.preventDefault();
    const itemType = document.getElementById('item_type').value;
    const amount = parseInt(document.getElementById('amount').value);

    try {
        await makeAPIRequest('addToShoppingList', 'PUT', { itemType, amount });
        location.reload();
    } catch (error) {
        alert('Failed to add item to shopping list');
    }
}

async function removeFromList(itemType, amount) {
    try {
        await makeAPIRequest('removeFromShoppingList', 'DELETE', { itemType });
        location.reload();
    } catch (error) {
        alert('Failed to remove item from shopping list');
    }
}

async function confirmPurchase() {
    const amount = parseInt(document.getElementById('purchaseAmount').value);
    const expirationDate = document.getElementById('purchaseExpiration').value;

    if (amount > currentMaxAmount) {
        alert(`Cannot purchase more than ${currentMaxAmount} items`);
        return;
    }

    try {
        await makeAPIRequest('purchaseItem', 'PATCH', {
            itemType: currentPurchaseItemType,
            amount: amount,
            expirationDate: expirationDate
        });
        $('#purchaseModal').modal('hide');
        location.reload();
    } catch (error) {
        alert('Failed to purchase item');
    }
} 