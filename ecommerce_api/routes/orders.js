const express = require('express');
const router = express.Router();
const Order = require('../models/Order');

// Créer une commande
router.post('/', async (req, res) => {
    try {
        const order = new Order(req.body);
        await order.save();
        res.status(201).json(order);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Obtenir toutes les commandes d'un utilisateur
router.get('/:userId', async (req, res) => {
    try {
        const orders = await Order.find({ userId: req.params.userId });
        res.json(orders);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
