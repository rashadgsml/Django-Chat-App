// Notification socket
var loc = window.location
var wsStart = "ws://"
if (loc.protocol == "https:"){
    wsStart = "wss://"
    }

var webSocketEndpoint =  wsStart + loc.host

var notificationSocket = new WebSocket(webSocketEndpoint)

notificationSocket.onmessage = function(e){
    var data = JSON.parse(e.data);
    console.log(data);
    
    Toast.show(`${data['from']}`+': '+`${data['content']}`);

}
