const socket = io(ENDPOINT, {
  transports: ['websocket'],
  withCredentials: true,
});

socket.on('connect', function () {
  let room_id = document.getElementById("room_id").value;
  socket.emit('joined', { room: room_id });
});

document.getElementById("messageForm").addEventListener("submit", function (event) {
  event.preventDefault();
  let message = document.getElementById("message").value;
  let room_id = document.getElementById("room_id").value;
  console.log(`Emitting message: ${message} to room: ${room_id}`); // Debugging line
  socket.emit('text', { msg: message, room: room_id });
  document.getElementById("message").value = "";
});

socket.on('message', function (data) {
  let ul = document.getElementById("chatMessages");
  let li = document.createElement("li");
  li.appendChild(document.createTextNode(data.msg));
  ul.appendChild(li);
  ul.scrollTop = ul.scrollHeight;
});

socket.on('status', function (data) {
  let ul = document.getElementById("chatMessages");
  let li = document.createElement("li");
  li.className = "status";
  li.appendChild(document.createTextNode(data.msg));
  ul.appendChild(li);
  ul.scrollTop = ul.scrollHeight;
});

// When the user leaves the page
window.addEventListener('beforeunload', function () {
  let room_id = document.getElementById("room_id").value;
  socket.emit('left', { room: room_id });
});