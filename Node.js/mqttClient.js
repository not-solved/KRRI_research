var mqtt = require('mqtt');
const MQTT_ADDR = "mqtt://192.168.10.193"
const options = {
    // host: '192.168.10.193', 
    // port: 1883,
    clientId: "mqttjs01",
    username: 'mqttdev',
    password: 'dev123'
}

function MQTT_msg_parse(com, board, block1, block2, block3, block4) {
    result = [];
    result.push(com);
    // result.push(board);
    boards = [block1, block2, block3, block4];
    boards.forEach((b) => {
        result.push(parseInt(b.substring(43, 45)))
        /*
        result.push([
            b.substring(16, 19),
            b.substring(19, 22),
            b.substring(22, 25),
            b.substring(25, 28)
        ]);
        */
        result.push(b.substring(16, 19));
        result.push(b.substring(19, 22));
        result.push(b.substring(22, 25));
        result.push(b.substring(25, 28));
    });
    return result
}

topic_list = ['pubSBK006', 'pubSBK007', 'pubSBK008', 'pubSBK009', 'pubSBK010',
'pubSBK011', 'pubSBK012', 'pubSBK013', 'pubSBK014', 'pubSBK015']

var client  = mqtt.connect("mqtt://192.168.10.193:1883", options);

//  연결
client.on('connect', () => {
    console.log("connected flag : " + client.connected)
    client.subscribe(topic_list, 1);
})

client.on("error", (err) => {
    console.log("Connection error : " + err)
    client.end()
})


client.on('message', (topic, message) => { 
    msg = message.toString()
    console.log(MQTT_msg_parse(msg.substring(10, 14), msg.substring(26, 30), msg.substring(43, 89),
                           msg.substring(93, 139), msg.substring(143, 189), msg.substring(193, 239)))
})

/*
var mysql = require('mysql');

const IP = '192.168.10.193';
const PORT = 3306;

const USER = 'krri';
const PASSWORD = 'Mobility408';

var connection = mysql.createConnection({
    host : IP,
    port : PORT,
    user : USER,
    password : PASSWORD,
    database : 'smartBlock',
    debug : false
});

const lcDB = 'sb_block_lc';
const bleDB = 'sb_user_block_ble';

var BLEdata = new Array();

connection.query(
    'SELECT no, block_id, minor, rssi, reg_dt FROM sb_user_block_ble WHERE reg_dt > \'2021-8-23 14:00\'',
    (error, result, fields) => {
        if(error) {
            throw error;
        }
        
        BLEdata = Object.values(JSON.parse(JSON.stringify(result)));
        BLEdata.forEach(data => {
            data.no = parseInt(data.no);
            data.block_id = parseInt(data.block_id);
            data.minor = parseInt(data.minor);
            data.rssi = parseInt(data.rssi);
            data.reg_dt = new Date(data.reg_dt);
        });
        BLEdata.forEach(data => console.log(data))
});

var LCdata = new Array();

connection.query(
    'SELECT minor, lc1, lc2, lc3, lc4, reg_dt FROM sb_block_lc where reg_dt > \'2021-8-23 14:00\'',
    (err, result, fields) => {
        if(err) {
            throw err;
        }

        LCdata = Object.values(JSON.parse(JSON.stringify(result)));
        LCdata.forEach(data => {
            data.minor = parseInt(data.minor);
            data.lc1 = parseInt(data.lc1);
            data.lc2 = parseInt(data.lc2);
            data.lc3 = parseInt(data.lc3);
            data.lc4 = parseInt(data.lc4);
            data.reg_dt = new Date(data.reg_dt);
        })
        LCdata.forEach(data => console.log(data))
    }
);

connection.end();
*/
