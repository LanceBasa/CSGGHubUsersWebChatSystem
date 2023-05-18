document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready!');

    const socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    console.log('check1', socket.connected)

    socket.on('connect', function(){
        console.log("connected", socket.connected)
        socket.emit('my event', {data:"Brother"});
    })

    document.getElementById("message").addEventListener("keyup", function(event){
        if (event.key=="Enter"){
            let message = document.getElementById("message").value;
            socket.emit("new_message",message);
            document.getElementById("message").value="";
        }
    })

    socket.on("chat", function(data) {
        console.log(data["message"]);
        appendMessage(data["message"], data["username"]);
    })
    
    socket.on("load_messages", function(messages) {
        for(let message of messages) {
            appendMessage(message.text, message.username);
        }
    })
    

    function appendMessage(message, username) {
        let ul = document.getElementById("chatMessages");
        let li = document.createElement("li");
        let textNode = document.createTextNode(username + ": " + message);
        li.appendChild(textNode);
        ul.appendChild(li);
        ul.scrollTop = ul.scrollHeight;
    }
    
});
