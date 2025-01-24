const express = require('express');
const router = express.Router();
const fridgeController = require('../controllers/fridgeController');

// Individual Items routes
router.put('/api/v1/addItem', fridgeController.addItem);
router.delete('/api/v1/removeItem', fridgeController.removeItem);
router.delete('/api/v1/removeItems', fridgeController.removeItems);

// Item Types routes
router.put('/api/v1/newType', fridgeController.newType);
router.delete('/api/v1/removeType', fridgeController.removeType);

// Shopping List routes
router.put('/api/v1/addToShoppingList', fridgeController.addToShoppingList);
router.delete('/api/v1/removeFromShoppingList', fridgeController.removeFromShoppingList);
router.patch('/api/v1/purchaseItem', fridgeController.purchaseItem);

module.exports = router; 