const mongoose = require('mongoose');
require('dotenv').config()


const dbConnect=()=>{
    mongoose.connect(process.env.Database_Url, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    }).then(console.log("Db Connected Successfully")).catch((error)=>{  
        console.log("error aagya db connect krne me");
        console.log(error);
        process.exit(1);
    })
};
module.exports=dbConnect;