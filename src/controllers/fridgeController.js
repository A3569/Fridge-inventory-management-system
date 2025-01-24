const db = require('../database/db'); // You'll need to set up your database connection

const fridgeController = {
    // Add item to fridge
    addItem: async (req, res) => {
        try {
            const { itemType, expirationDate, amount } = req.body;
            
            // Validate input
            if (!itemType || !expirationDate || !amount) {
                return res.status(400).json({ error: 'Missing required fields' });
            }

            // Check if item type exists
            const typeExists = await db.ItemTypes.findOne({ where: { id: itemType }});
            if (!typeExists) {
                return res.status(404).json({ error: 'Item type not found' });
            }

            await db.IndividualItems.create({
                itemType,
                expirationDate,
                amount
            });

            res.status(200).json({ message: 'Item added successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Remove single item from fridge
    removeItem: async (req, res) => {
        try {
            const { ID } = req.body;
            
            const deleted = await db.IndividualItems.destroy({
                where: { id: ID }
            });

            if (!deleted) {
                return res.status(404).json({ error: 'Item not found' });
            }

            res.status(200).json({ message: 'Item removed successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Remove multiple items from fridge
    removeItems: async (req, res) => {
        try {
            const { items } = req.body;
            const ids = items.map(item => item.ID);

            const deleted = await db.IndividualItems.destroy({
                where: { id: ids }
            });

            res.status(200).json({ message: `${deleted} items removed successfully` });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Create new item type
    newType: async (req, res) => {
        try {
            const { uniqueBarcode, name, amountType } = req.body;

            // Check if barcode already exists
            const existing = await db.ItemTypes.findOne({
                where: { uniqueBarcode }
            });

            if (existing) {
                return res.status(400).json({ error: 'Barcode already exists' });
            }

            await db.ItemTypes.create({
                uniqueBarcode,
                name,
                amountType
            });

            res.status(200).json({ message: 'Item type created successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Remove item type
    removeType: async (req, res) => {
        try {
            const { uniqueBarcode } = req.body;

            // Check if any items of this type exist in fridge
            const existingItems = await db.IndividualItems.findOne({
                where: { itemType: uniqueBarcode }
            });

            if (existingItems) {
                return res.status(400).json({ 
                    error: 'Cannot remove type while items of this type exist in fridge' 
                });
            }

            const deleted = await db.ItemTypes.destroy({
                where: { uniqueBarcode }
            });

            if (!deleted) {
                return res.status(404).json({ error: 'Item type not found' });
            }

            res.status(200).json({ message: 'Item type removed successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Add item to shopping list
    addToShoppingList: async (req, res) => {
        try {
            const { itemType, amount } = req.body;

            const existing = await db.ShoppingList.findOne({
                where: { itemType }
            });

            if (existing) {
                await existing.update({
                    amount: existing.amount + amount
                });
            } else {
                await db.ShoppingList.create({
                    itemType,
                    amount
                });
            }

            res.status(200).json({ message: 'Shopping list updated successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Remove item from shopping list
    removeFromShoppingList: async (req, res) => {
        try {
            const { itemType, amount } = req.body;

            const item = await db.ShoppingList.findOne({
                where: { itemType }
            });

            if (!item) {
                return res.status(404).json({ error: 'Item not found in shopping list' });
            }

            const newAmount = item.amount - amount;
            if (newAmount <= 0) {
                await item.destroy();
            } else {
                await item.update({ amount: newAmount });
            }

            res.status(200).json({ message: 'Shopping list updated successfully' });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    },

    // Purchase item (move from shopping list to fridge)
    purchaseItem: async (req, res) => {
        try {
            const { itemType, amount, expirationDate } = req.body;

            // Add to inventory
            await db.IndividualItems.create({
                itemType,
                amount,
                expirationDate
            });

            // Remove from shopping list
            await db.ShoppingList.destroy({
                where: {
                    itemType
                }
            });

            res.status(200).json({ message: 'Item purchased successfully' });
        } catch (error) {
            console.error('Error purchasing item:', error);
            res.status(500).json({ error: 'Failed to purchase item' });
        }
    }
};

module.exports = fridgeController; 