const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the same directory as server.js
app.use(express.static(path.join(__dirname, '../website')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});


module.exports = app;
