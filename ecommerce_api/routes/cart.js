const express = require('express');
const router = express.Router();
const Cart = require('../models/Cart');
const Product = require('../models/Product');

// Ajouter un produit au panier
router.post('/:userId', async (req, res) => {
    try {
        const { productId, quantity } = req.body;
        let cart = await Cart.findOne({ userId: req.params.userId });

        if (!cart) {
            cart = new Cart({ userId: req.params.userId, products: [] });
        }

        const productIndex = cart.products.findIndex(p => p.productId.toString() === productId);
        if (productIndex > -1) {
            cart.products[productIndex].quantity += quantity;
        } else {
            cart.products.push({ productId, quantity });
        }

        await cart.save();
        res.status(200).json(cart);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Récupérer le panier d'un utilisateur
router.get('/:userId', async (req, res) => {
    try {
        const cart = await Cart.findOne({ userId: req.params.userId }).populate('products.productId');
        if (!cart) return res.status(404).json({ message: "Panier non trouvé" });
        res.json(cart);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Supprimer un produit du panier
router.delete('/:userId/item/:productId', async (req, res) => {
    try {
        let cart = await Cart.findOne({ userId: req.params.userId });
        if (!cart) return res.status(404).json({ message: "Panier non trouvé" });

        cart.products = cart.products.filter(p => p.productId.toString() !== req.params.productId);
        await cart.save();
        res.json(cart);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;  // ✅ Assurez-vous que cette ligne est bien présente !
