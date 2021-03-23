function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



var loc = window.location
var wsStart = "ws://"
if (loc.protocol == "https:"){
    wsStart = "wss://"
    }

var webSocketEndpoint =  wsStart + loc.host + '/ws/chat/' +
    roomName +
    '/'

var chatSocket = new WebSocket(webSocketEndpoint)

//const chatSocket = new WebSocket(
//    'ws://'
//    + window.location.host
//    + '/ws/chat/'
//    + roomName
//    + '/'
//);

chatSocket.onopen = function(e){
    fetchMessages();
}

chatSocket.onmessage = function(e) {
    var data = JSON.parse(e.data);
    var request_user = username;
    if (data['command'] === 'messages'){
        for (let i=data['messages'].length-1; i>=0; i--){
            createMessage(data['messages'][i]);
        }
        try{
            for (let i=0; i<data['rooms'].length; i++){
                document.getElementById(`preview-${data['rooms'][i]['room_id']}`).innerHTML = (`${data['rooms'][i]['messages'][data['rooms'][i]['messages'].length - 1]['author']}: ${data['rooms'][i]['messages'][data['rooms'][i]['messages'].length - 1]['content']}`);
                for (let j=0; j<data['rooms'][i]['participants'].length; j++){
                    if (data['rooms'][i]['participants'][j]['username'] !== request_user){
                        document.getElementById(`status-${data['rooms'][i]['room_id']}`).className = `contact-status ${data['rooms'][i]['participants'][j]['status']}`;
                    }
                }
            }
        }catch{
            console.error('error');
        }
        updateScroll();
    }
    else if (data['command'] === 'new_message'){
        createMessage(data['message']);
        try{
        for (let i=0; i<data['rooms'].length; i++){
            document.getElementById(`preview-${data['rooms'][i]['room_id']}`).innerHTML = (`${data['rooms'][i]['messages'][data['rooms'][i]['messages'].length - 1]['author']}: ${data['rooms'][i]['messages'][data['rooms'][i]['messages'].length - 1]['content']}`);
            for (let j=0; j<data['rooms'][i]['participants'].length; j++){
                if (data['rooms'][i]['participants'][j]['username'] !== request_user){
                    document.getElementById(`status-${data['rooms'][i]['room_id']}`).className = `contact-status ${data['rooms'][i]['participants'][j]['status']}`
                }
            }
        }
        }
        catch{
            console.log('error');
        }
        notificationSocket.send(JSON.stringify({'from':data['message']['author'],'content':data['message']['content'],'timestamp':data['message']['timestamp']}))
        updateScroll();
    }

    for (let i=0; i<data['rooms'].length; i++){
        document.querySelector(`#id-${data['rooms'][i]['room_id']}-submit`).onclick = function(e) {
            window.location.pathname = `/chat/${data['rooms'][i]['room_name']}/`;
        };
    }

};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    
    chatSocket.send(JSON.stringify({
        'message': message,
        'command': 'new_message',
        'from': username,
        'room_name': roomName
    }));
    messageInputDom.value = '';
};

function fetchMessages(){
    chatSocket.send(JSON.stringify({'command':'fetch_messages','room_name':roomName}));
}

function createMessage(data){
    var author = data['author'];
    var msgListTag = document.createElement('li')
    var imgTag = document.createElement('img');
    var pTag = document.createElement('p');
    pTag.textContent = data.content;
    imgTag.src = "http://emilcarlsson.se/assets/harveyspecter.png";

    if (author === username){
        msgListTag.className = 'sent';
    }
    else{
        msgListTag.className = 'replies';
    }
    msgListTag.appendChild(imgTag);
    msgListTag.appendChild(pTag);
    document.querySelector('#chat-log').appendChild(msgListTag);
}

function updateScroll(){
    var element = document.getElementById("chat-area");
    element.scrollTop = element.scrollHeight;
}

var webSocketEndpoint =  wsStart + loc.host

var notificationSocket = new WebSocket(webSocketEndpoint)
