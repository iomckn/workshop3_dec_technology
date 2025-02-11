require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;
const productRoutes = require('./routes/products');
const orderRoutes = require('./routes/orders');
const cartRoutes = require('./routes/cart');

app.use('/products', productRoutes);
app.use('/orders', orderRoutes);
app.use('/cart', cartRoutes);


// Middleware
app.use(cors());
app.use(express.json());

// Connexion à MongoDB
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("✅ Connecté à MongoDB"))
    .catch(err => console.error("❌ Erreur de connexion MongoDB:", err));

// Routes principales
app.get('/', (req, res) => res.send('API e-commerce fonctionne 🚀'));

app.listen(PORT, () => console.log(`✅ Serveur en cours d'exécution sur http://localhost:${PORT}`));

