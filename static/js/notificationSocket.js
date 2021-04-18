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
    const audio = new Audio('/./static/audio/notification_sound.ogg');
  
    audio.play();
    
    Toast.show(`${data['from']}`+': '+`${data['content']}`,'success');
    
}
