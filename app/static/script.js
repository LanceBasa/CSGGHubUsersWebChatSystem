document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready!');

    const socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    console.log('check if connected', socket.connected)

    socket.on('connect', function(){
        console.log("connected", socket.connected)
        socket.emit('join', {data:"username"});
    })

    document.getElementById("message").addEventListener("keyup", function(event){
        let message = document.getElementById("message").value;
        if (event.key=="Enter" && message != ''){
            socket.emit("new_message",message);
            document.getElementById("message").value="";
        }
    })

    socket.on("chat", function(data) {
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
        li.classList.add("userChat");
        let textNode = null;
      
        if (username == 'System') {
          message = message.replace(/,/g, "<br>");
          li.style.color = "darkgreen"; // Set text color to dark green
          li.innerHTML = message;
        } else {
          textNode = document.createTextNode(username + ": " + message);
          li.appendChild(textNode);
        }
      
        ul.appendChild(li);
        ul.lastElementChild.scrollIntoView({ behavior: "smooth" }); // Scroll to the bottom
      }
      






  });

  


