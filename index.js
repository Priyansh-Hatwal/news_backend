const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const axios = require('axios');
const mongoose = require('mongoose');
require('dotenv').config()
const dbConnect = require("./config/database");
dbConnect();
const News = require("./models/newsModel");

const app = express();
const port = process.env.PORT||5000

app.use(cors());

let cache = {
    data: null,   
    timestamp: 0  
};

const CACHE_DURATION = 5 * 60 * 1000; 

const scrapeAndUpdateCache = async () => {
    try {
        console.log("Called the function at ",Date.now())
        exec('python Homepage.py', { maxBuffer: 1024 * 1024 * 10 }, async (error, stdout, stderr) => {
            if (error) {
                console.error(`Error: ${error}`);
                return;
            }
            const newsArray = await News.find().sort({ scraped_at: -1 }).exec();

            if (newsArray.length === 0) {
                console.log('No news data available');
                return;
            }

            cache.data = newsArray;
            cache.timestamp = Date.now();
            console.log('Cache updated with new data');
        });
    } catch (err) {
        console.error(err);
    }
};

scrapeAndUpdateCache();
setInterval(scrapeAndUpdateCache, 12 * 60 * 60 * 1000);

app.get('/scrape-news', (req, res) => {
    const currentTime = Date.now();
    if (cache.data && (currentTime - cache.timestamp) < CACHE_DURATION) {
        return res.json(cache.data);  
    }
    res.json({ message: 'Data is being fetched, please try again shortly.' });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
