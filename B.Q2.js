const express = require('express');
const app = express();
const PORT = 3001; // Port du serveur DNS

app.get('/getServer', (req, res) => {
    res.json({
        code: 200,
        server: `localhost:${PORT}`
    });
});

app.listen(PORT, () => {
    console.log(`DNS Registry running at http://localhost:${PORT}`);
});
