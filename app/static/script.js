
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready!');

    const socket =io.connect('http://' + document.domain + ':' + location.port + '/chat');//maybe??
    //const socket =io.connect('')
    //const socket =io.connect('')
    console.log('check1', socket.connected)



    socket.on('connect',function(){
        console.log("connected", socket.connected)

        //socket.emit("user_join", 'Brother');
    })

    document.getElementById("message").addEventListener("keyup", function(event){
        if (event.key=="Enter"){
            alert("works");
            let message = document.getElementById("message").value;
            socket.emit("new_message",message);
            document.getElementById("message").value="";
        }
    })

    socket.on("chat", function(data) {
        alert("works 2")

        console.log(data["message"]);
        let ul = document.getElementById("chatMessages");
        let li = document.createElement("li");
        li.appendChild(document.createTextNode(data["message"]));
        ul.appendChild(li);
        ul.scrolltop = ul.scrollHeight;
    })


  });