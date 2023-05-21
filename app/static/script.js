document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready!');

    // Connect to the socket.io server
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    console.log('check if connected', socket.connected)

    // When connected to the socket.io server
    socket.on('connect', function(){
        console.log("connected", socket.connected)
        socket.emit('join', {data:"username"});
    })

    // Listen for keyup event on the message input field
    document.getElementById("message").addEventListener("keyup", function(event){
        let message = document.getElementById("message").value;
        if (event.key=="Enter" && message != ''){
            socket.emit("new_message",message);
            document.getElementById("message").value="";
        }
    })
    // Receive chat event from the server
    socket.on("chat", function(data) {
        appendMessage(data.message, data.username, data.created_at);
    });
    
    
    

    // Receive load_messages event from the server
    socket.on("load_messages", function(messages) {
        // Load and display existing messages
        for (let message of messages) {
            appendMessage(message.text, message.username, message.created_at);
        }
    });
    

    // Listen for keyup event on the search input field
    document.getElementById('search').addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            var searchQuery = this.value;
            socket.emit('search_message', { searchQuery: searchQuery, page: 1 });
        }
    });


    // Handle search results from the server &  Receive search_results event from the server
    socket.on("search_results", function(results) {
        document.getElementById('chatMessages').innerHTML = "";
    
        for (var i = 0; i < results.length; i++) {
            var message = results[i];
            appendMessage(message.text, message.username, message.created_at);
        }
    });
    
    // Function to append a new message to the chat are
    function appendMessage(message, username, created_at) {
        let ul = document.getElementById("chatMessages");
        let li = document.createElement("li");
        li.classList.add("userChat");
        let textNode = null;
        if (username == 'System') {
            // Handle system messages
            message = message.replace(/,/g, "<br>");
            li.style.color = "darkgreen"; // Set text color to dark green
            li.innerHTML = message;
          } else {
            // Handle user messages
            let timestamp = created_at ? '[' + formatDate(new Date(created_at)) + '] ' : "";
        let usernameLink = document.createElement("a");
        usernameLink.href = "/profile/" + username; // Replace "/profile/" with the actual URL of the user profile
        usernameLink.textContent = username;
        let messageText = document.createTextNode(": " + message);
        li.appendChild(document.createTextNode(timestamp));
        li.appendChild(usernameLink);
        li.appendChild(messageText);
        }
        ul.appendChild(li);
        ul.lastElementChild.scrollIntoView({ behavior: "smooth" });
      }
      
      // Function to format the date in a desired format
      function formatDate(date) {
        const options = { day: "2-digit", month: "2-digit", year: "2-digit", hour: "2-digit", minute: "2-digit" };
        return date.toLocaleString("en-Au", options).replace(',', '');
      }
    
});
