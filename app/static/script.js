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
        appendMessage(data.message, data.username, data.created_at);
    });
    
    
    
    socket.on("load_messages", function(messages) {
        console.log(messages);
        for (let message of messages) {
            appendMessage(message.text, message.username, message.created_at);
        }
    });
    

    // Listen for keyup event on the search input field
    // Listen for keyup event on the search input field
    document.getElementById('search').addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            var searchQuery = this.value;
            socket.emit('search_message', { searchQuery: searchQuery, page: 1 });
        }
    });


    // Handle search results from the server
    socket.on("search_results", function(results) {
        document.getElementById('chatMessages').innerHTML = "";
    
        for (var i = 0; i < results.length; i++) {
            var message = results[i];
            appendMessage(message.text, message.username, message.created_at);
        }
    });
    
    
    function appendMessage(message, username, created_at) {
        let ul = document.getElementById("chatMessages");
        let li = document.createElement("li");
        li.classList.add("userChat");
        let textNode = null;
        if (username === 'System') {
            textNode = document.createTextNode(message);
            li.style.color = "darkgreen";
        } else {
            let timestamp = created_at ? " (" + created_at + ")" : "";  // Check if created_at value is defined
            textNode = document.createTextNode(username + ": " + message + timestamp);
        }
        li.appendChild(textNode);
        ul.appendChild(li);
        ul.lastElementChild.scrollIntoView({ behavior: "smooth" });
    }
    
    
});
