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

function sendRequest(id) {
    try{
        val = document.getElementById(`send-${id}`).name;
        document.getElementById(`send-${id}`).value = 'Cancel friend request';
        document.getElementById(`send-${id}`).className = 'btn btn-danger';
        document.getElementById(`send-${id}`).id = `cancel-${id}`;
        notificationSocket.send(JSON.stringify({'command':'send_friend_request','to_id':id}))
    }
    catch{
        cancelRequest(id)
    }
  }

  function cancelRequest(id) {
    value = document.getElementById(`cancel-${id}`).name;
    
    document.getElementById(`cancel-${id}`).id = `send-${id}`;
    document.getElementById(`send-${id}`).className = 'btn btn-warning';
    document.getElementById(`send-${id}`).value = 'Send friend request';
    notificationSocket.send(JSON.stringify({'command':'cancel_friend_request','to_id':id}))
  }

  function like(x) {
      // fa fa-thumbs-up
      // fa fa-thumbs-up fa-thumbs-down
    x.classList.toggle("fa-thumbs-down");
  }