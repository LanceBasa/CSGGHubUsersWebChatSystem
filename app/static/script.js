
document.addEventListener('DOMContentLoaded', function() {
    console.log('Document is ready!');

    const socket =io.connect('http://' + document.domain + ':' + location.port + '/chat');//maybe??
    //const socket =io.connect('')
    //const socket =io.connect('')
    console.log('check1', socket.connected)



    socket.on('connect',function(){
        console.log("connected", socket.connected)

        socket.emit('my event', {data:"Brother"});
    })

    document.getElementById("message").addEventListener("keyup", function(event){
        let message = document.getElementById("message").value;
        if (event.key=="Enter" && message != ''){
            socket.emit("new_message",message);
            document.getElementById("message").value="";

        }
    })

    socket.on("chat", function(data) {

        console.log(data["message"]);
        let ul = document.getElementById("chatMessages");
        let li = document.createElement("li");
        li.classList.add("userChat");

        li.appendChild(document.createTextNode(data["message"]));
        ul.appendChild(li);
        //ul.scrollTop = ul.scrollHeight;
        ul.lastElementChild.scrollIntoView({ behavior: "smooth" }); // Scroll to the bottom

    })


  });

//   $(document).ready(function(){
//     var socket = io();
//     socket.on('my response', function(msg) {
//         $('#log').append('<p>Received: ' + msg.data + '</p>');
//     });
//     $('form#emit').submit(function(event) {
//         socket.emit('my event', {data: $('#emit_data').val()});
//         return false;
//     });
//     $('form#broadcast').submit(function(event) {
//         socket.emit('my broadcast event', {data: $('#broadcast_data').val()});
//         return false;
//     });
// });