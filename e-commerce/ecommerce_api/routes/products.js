const express = require('express');
const router = express.Router();
const Product = require('../models/Product');

// Obtenir tous les produits
router.get('/', async (req, res) => {
    try {
        const products = await Product.find(req.query);
        res.json(products);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Obtenir un produit par ID
router.get('/:id', async (req, res) => {
    try {
        const product = await Product.findById(req.params.id);
        if (!product) return res.status(404).json({ message: "Produit non trouvé" });
        res.json(product);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Ajouter un produit
router.post('/', async (req, res) => {
    try {
        const product = new Product(req.body);
        await product.save();
        res.status(201).json(product);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Mettre à jour un produit
router.put('/:id', async (req, res) => {
    try {
        const product = await Product.findByIdAndUpdate(req.params.id, req.body, { new: true });
        res.json(product);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// Supprimer un produit
router.delete('/:id', async (req, res) => {
    try {
        await Product.findByIdAndDelete(req.params.id);
        res.json({ message: "Produit supprimé avec succès" });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
