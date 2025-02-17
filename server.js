const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const templatesPath = path.join(__dirname, 'templates');
console.log("Templates Path:", templatesPath);

app.use(express.static(templatesPath));  // Serve static files
app.use(express.static(path.join(__dirname, 'static')));

// Database connection setup
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Simeon1405x',
    database: 'momo_database'
});

// Connect to the database
db.connect((err) => {
    if (err) {
        console.error('Database connection failed:', err);
        process.exit(1);
    }
    console.log('Successfully connected to MySQL database');
});

// Serve index.html from the templates folder
app.get('/', (req, res) => {
    res.sendFile(path.join(templatesPath, 'index.html'));
});

app.set('views', templatesPath); // Set the templates directory
app.set('view engine', 'ejs');   // Use EJS (or remove this if just serving static HTML)

// Render statistics page
app.get('/statistics', (req, res) => {
    res.render('statistics'); // Render without `.html`
});

// API for recent transactions
app.get('/api/recent-transactions', (req, res) => {
    const query = `
        SELECT transaction_id, category, sms_body, 
               DATE_FORMAT(sms_date, '%Y-%m-%d') AS date, 
               TIME_FORMAT(sms_time, '%H:%i:%s') AS time, 
               amount, 
               type  
        FROM transactions 
        ORDER BY sms_date DESC, sms_time DESC 
        LIMIT 1689`;

    db.query(query, (err, rows) => {
        if (err) {
            console.error('Database Query Error:', err);
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// New API endpoint to fetch data for charts
app.get('/api/chart-data', (req, res) => {
    const query = `
        SELECT sms_date, amount, category 
        FROM transactions 
        WHERE amount IS NOT NULL`;

    db.query(query, (err, rows) => {
        if (err) {
            console.error('Database Query Error:', err);
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

app.get('/api/chart-data', (req, res) => {
    const query = `
        SELECT sms_date, amount, category 
        FROM transactions 
        WHERE amount IS NOT NULL`;

    db.query(query, (err, rows) => {
        if (err) {
            console.error('Database Query Error:', err);
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});