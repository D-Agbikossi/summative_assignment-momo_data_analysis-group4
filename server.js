const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const path = require('path');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));  // Serve static files

// Database connection
const db = mysql.createConnection({
    host: '127.0.0.1',
    user: 'root',  
    password: 'Simeon1405x', 
    database: 'momo_database'
});

// Connect to database
db.connect((err) => {
    if (err) {
        console.error('Error connecting to database:', err);
        return;
    }
    console.log('Connected to database');
});

// Route for the home page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Route for the statistics page
app.get('/statistics', (req, res) => {
    res.sendFile(path.join(__dirname, 'statistics.html'));
});

// API endpoints
app.get('/api/transaction-summary', (req, res) => {
    const query = `
        SELECT 
            SUM(CASE WHEN type = 'incoming' THEN 1 ELSE 0 END) as incomings,
            SUM(CASE WHEN type = 'outgoing' THEN 1 ELSE 0 END) as outgoings,
            SUM(CASE WHEN type = 'withdrawal' THEN 1 ELSE 0 END) as withdrawals,
            SUM(CASE WHEN type = 'bill' THEN 1 ELSE 0 END) as bills
        FROM transactions`;
    
    db.query(query, (err, results) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(results[0]);
    });
});

app.get('/api/recent-transactions', (req, res) => {
    const query = 'SELECT * FROM transactions ORDER BY date DESC, time DESC LIMIT 10';
    db.query(query, (err, results) => {
        if (err) {
            res.status(500).json({ error: err.message });
            return;
        }
        res.json(results);
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
}); 