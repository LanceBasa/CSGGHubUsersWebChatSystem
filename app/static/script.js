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

    // Listen for keyup event on the search input field
    // Listen for keyup event on the search input field
    document.getElementById('search').addEventListener('keyup', function() {
        var searchQuery = this.value;
        socket.emit("search_message", {query: searchQuery, page: 1});
    })


    // Handle search results from the server
    socket.on("search_results", function(results) {
        // Clear existing chat messages
        document.getElementById('messages').innerHTML = "";
    
        // Add each result to the chat window
        for (var i = 0; i < results.length; i++) {
            var message = results[i];
            var node = document.createElement('li');
            node.textContent = message.username + ": " + message.text;
            document.getElementById('messages').appendChild(node);
        }
    });
    
    
    function appendMessage(message, username) {
        let ul = document.getElementById("chatMessages");
        let li = document.createElement("li");
        li.classList.add("userChat");
        let textNode=null;
        if (username=='System'){
            textNode = document.createTextNode(message);
            li.style.color = "darkgreen"; // Set text color to red
        }else {
            textNode = document.createTextNode(username + ": " + message);
        }
        li.appendChild(textNode);
        ul.appendChild(li);
        ul.lastElementChild.scrollIntoView({ behavior: "smooth" }); // Scroll to the bottom
    }
});
