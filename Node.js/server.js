var express = require('express');
var app = express();

const PORT = 3010;

app.listen(PORT, () => {
    console.log(`Open server on port ${PORT}`);
})

app.get('/', (req, res) => {

})

app.post('/', (req, res) => {
    var inputData;
    console.log(req.body);
})

