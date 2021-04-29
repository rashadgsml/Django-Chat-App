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
        $('#search-input').on('keyup', function(){
            var value = $(this).val();
            var searched_data = searchContact(value, data['rooms'])
            buildContacts(searched_data)
        })
        buildContacts(data['rooms']);
        for (let i=data['messages'].length-1; i>=0; i--){
            createMessage(data['messages'][i]);
        }
        
        updateScroll();
    }
    
    else if (data['command'] === 'new_message'){
        if (data['message']['author'] != request_user){
            createMessage(data['message']);
        }
        updateScroll();
        var myRooms = []
        for (i in data['all_rooms']){
            for (j in data['all_rooms'][i]['participants']){
                if(request_user == data['all_rooms'][i]['participants'][j]['username']){
                    myRooms.push(data['all_rooms'][i])
                }
            }
        }
        try{
            for (let i=0; i<myRooms.length; i++){
                document.getElementById(`preview-${myRooms[i]['room_id']}`).innerHTML = (`${myRooms[i]['messages'][myRooms[i]['messages'].length - 1]['author']}: ${myRooms[i]['messages'][myRooms[i]['messages'].length - 1]['content']}`);
                for (let j=0; j<myRooms[i]['participants'].length; j++){
                    if (myRooms[i]['participants'][j]['username'] !== request_user){
                        if(myRooms[i]['room_name'] == roomName){
                            to_profile = myRooms[i]['participants'][j]['username'];
                        }
                        document.getElementById(`status-${myRooms[i]['room_id']}`).className = `contact-status ${myRooms[i]['participants'][j]['status']}`
                    }
                }
            }
        }
        catch{
            console.error('error');
        }
        notificationSocket.send(JSON.stringify({'type':'message_notification','from':data['message']['author'],'to':to_profile,'content':data['message']['content'],'timestamp':data['message']['timestamp']}))

        $('#search-input').on('keyup', function(){
            var value = $(this).val();
            var searched_data = searchContact(value, myRooms)
            buildContacts(searched_data)
        })
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
    createMessageImmidietly(username, message)
    updateScroll()
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

function buildContacts(rooms){
    $('#rooms').empty();
    for (let i=0; i<rooms.length; i++){
        var contactListTag = document.createElement('li')
        contactListTag.className = 'contact'

        var divWrap = document.createElement('div')
        divWrap.className = 'wrap'

        var contactSpan = document.createElement('span')
        contactSpan.className = 'contact-status busy'

        var contactImg = document.createElement('img')
        contactImg.src = "http://emilcarlsson.se/assets/harveyspecter.png"

        var divMeta = document.createElement('div')
        divMeta.className = 'meta'

        namePTag = document.createElement('p')
        namePTag.className = 'name'

        previewPTag = document.createElement('p')
        previewPTag.className = 'preview'
        
        contactListTag.id = `id-${rooms[i]['room_id']}-submit`
        if (currentRoomName == rooms[i]['room_name']){
            contactListTag.className = 'contact active'
        }
        contactSpan.id = `status-${rooms[i]['room_id']}`
        namePTag.id = `id-${rooms[i]['room_id']}`
        if (rooms[i]['participants'].length == 2){
            for (let j=0; j<rooms[i]['participants'].length; j++){
                if (rooms[i]['participants'][j]['username'] != profile_username){
                    namePTag.textContent = rooms[i]['participants'][j]['username']
                }
            }
        }
        else{
            namePTag.textContent = rooms[i]['room_name']
        }
        previewPTag.id = `preview-${rooms[i]['room_id']}`

        divMeta.appendChild(namePTag)
        divMeta.appendChild(previewPTag)
        divWrap.appendChild(contactImg)
        divWrap.appendChild(contactSpan)
        divWrap.appendChild(divMeta)
        contactListTag.appendChild(divWrap)
        document.querySelector('#rooms').appendChild(contactListTag);
    }
    for (let i=0; i<rooms.length; i++){
        document.querySelector(`#id-${rooms[i]['room_id']}-submit`).onclick = function(e) {
            window.location.pathname = `/chat/${rooms[i]['room_name']}/`;
        };
    }
    var request_user = username;
    for (let i=0; i<rooms.length; i++){
        try{
            document.getElementById(`preview-${rooms[i]['room_id']}`).innerHTML = (`${rooms[i]['messages'][rooms[i]['messages'].length - 1]['author']}: ${rooms[i]['messages'][rooms[i]['messages'].length - 1]['content']}`);
            }
        catch{
            console.error('error');
        }
        for (let j=0; j<rooms[i]['participants'].length; j++){
            if (rooms[i]['participants'][j]['username'] !== request_user){
                document.getElementById(`status-${rooms[i]['room_id']}`).className = `contact-status ${rooms[i]['participants'][j]['status']}`;
            }
        }
    }
}

function createMessageImmidietly(author, content){
    var author = author;
    var msgListTag = document.createElement('li')
    var imgTag = document.createElement('img');
    var pTag = document.createElement('p');
    pTag.textContent = content;
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

function searchContact(value, data){
    var filteredData = []
    var request_user = username;
    var to_profile;
    
    for (var i=0; i<data.length; i++){
        for(var j=0; j<data[i]['participants'].length; j++){
            if(data[i]['participants'][j]['username'] != request_user){
                to_profile = data[i]['participants'][j]['username'];
            }
        }
        value = value.toLowerCase()
        
        var name = to_profile.toLowerCase()

        if(name.includes(value)){
            filteredData.push(data[i])
        }
        
    }
    return filteredData
}

var webSocketEndpoint =  wsStart + loc.host

var notificationSocket = new WebSocket(webSocketEndpoint)
