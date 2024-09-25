const mongoose = require('mongoose');

const NewsSchema = new mongoose.Schema({
    title: String,
    link: String,
    channel: String,
    image: String,
    figure: String,
    scraped_at: { type: Date, default: Date.now }
}, { collection: 'news_collection' });  

module.exports=mongoose.model('News', NewsSchema);