var express = require('express');
var app = express();

const PORT = 3010;

app.get('/ble', (req, res) => {

})

app.post('/post', (req, res) => {
    var inputData;
    req.on('data', (data) => {
        inputData = JSON.parse(data);
    })
})

app.listen(PORT, () => {
    console.log(`Open server on port ${PORT}`);
})