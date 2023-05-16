const socket =io.connect('http://localhost:5000');


socket.on('connect',function(){
    socket.emit("user_join", 'Brother');
})

document.getElementById("message").addEventListener("keyup", function(event){
    if (event.key=="Enter"){
        let message = document.getElementById("message").value;
        socket.emit("new_message",message);
        document.getElementById("message").value="";
    }
})

socket.on("chat", function(data){
    console.log(data["message"]);
    let ul = document.getElementById("chatMessages");
    let li = document.createElement("li");
    li.appendChild(document.createTextNode(data["message"]));
    ul.appendChild(li);
    ul.scrolltop = ul.scrollHeight;
})
