const express = require('express');
const fs = require('fs');
const csv = require('csv-parser');


const app = express();
const port = 555;

app.get('/', (req, res) => {
    res.send('Hello World 4');
});

app.get('/api/shops_data', (req, res) => {
    const results = [];
    try{
        fs.createReadStream('data-shops.csv')
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            res.json(results);
        });
    } catch (err) {
        res.status(500).send('Error reading data-shops');
    }
});

app.get('/api/products_data', (req, res) => {
    const results = [];
    try{
        fs.createReadStream('data-products.csv')
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            res.json(results);
        });
    } catch (err) {
        res.status(500).send('Error reading data-products');
    }
});
app.get('/api/sales_data', (req, res) => {
    const results = [];
    try{
        fs.createReadStream('data-sales.csv')
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
            res.json(results);
        });
    } catch (err) { 
        res.status(500).send('Error reading data-sales');   
    }
})
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});