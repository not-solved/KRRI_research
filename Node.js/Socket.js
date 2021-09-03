var express = require('express');
var app = express();
var Socket = require('socket.io');

const PORT = 3010;
var server = app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`)
});

var clients = []

server.on('connection', (socket) => {
    console.log("Connected");

    socket.on('msg', (data) => {
        console.log(data);
    })
})