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

app.use(express.static(templatesPath)); 



app.get('/', (req, res) => {
    res.sendFile('index.html', { root: __dirname });  
});


app.get('/statistics', (req, res) => {
    res.sendFile('statistics.html', { root: staticPath }); 
});


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

const db = mysql.createConnection({ 
    host: 'localhost',
    user: 'root',  
    password: 'Simeon1405x', 
    database: 'momo_database'
});

db.connect((err) => {
    if (err) {
        console.error('Database connection failed:', err);
        process.exit(1);
    }
    console.log('Successfully connected to MySQL database');
});


app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});