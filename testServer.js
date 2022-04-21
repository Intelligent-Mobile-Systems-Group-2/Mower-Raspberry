const WebSocketServer = require('ws');
const PORT = 8765;
 
const wss = new WebSocketServer.Server({ port: PORT })
 
wss.on("connection", ws => {
    console.log("new client connected");
    ws.on("message", data => {
        console.log(`Client has sent us: ${data}`)
    });
    ws.on("close", () => {
        console.log("the client has disconnected");
    });
    ws.onerror = function () {
        console.log("Some Error occurred")
    }
});
console.log("The WebSocket server is running on port" + PORT);  