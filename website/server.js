const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the same directory as server.js
app.use(express.static(__dirname));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/hello', (req, res) => {
    res.send(__dirname);
});


module.exports = app;
