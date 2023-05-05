 // Enable navigation prompt
 window.onbeforeunload = function() {
    socket.emit('leave')
    window.location.href = leaveUrl;
};
function preventBack(){window.history.forward();}
  setTimeout("preventBack()", 0);
  window.onunload=function(){null};

// JavaScript code for the chat room
const socket = io.connect();
const messageForm = document.querySelector('#message-form');
const messageInput = document.querySelector('#message-input');
const messagesContainer = document.querySelector('#messages');
const activeUsersContainer = document.querySelector('#active-users .user-container');
const logoutLink = document.querySelector('#logout-button');





let username;
fetch ('/get_username')
  .then(response => response.json())
  .then(data => {
    username=data.username;
  })
  .catch(error => {
    console.error('error getting username: ',error);
  });





// Event listener for submitting the message form
messageForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  if (text) {
    socket.emit('message', { message: text });
    messageInput.value = '';
    messageInput.focus();
  }
  
});

// Function to add a new message to the messages container
function addMessage(message) {
  console.log('New message:', message);
  const messageElement = document.createElement('div');
  if (message.username==username){
    messageElement.classList.add('my-message');
    messageElement.innerHTML = `<div class="badge bg-primary text-wrap" style="width: 100;">
    <p class="text-break" style="font-size:1.1rem;" >You:${message.message}</p></div>`;
  }
  else{
    messageElement.classList.add('message');
    messageElement.innerHTML = `<div class="badge bg-secondary text-wrap" style="width: 100;">
    <p class="text-break" style="font-size:1.1rem;" >${message.username}:${message.message}</p></div>`;
  }
  messagesContainer.appendChild(messageElement);
  var xH = messagesContainer.scrollHeight; 
  messagesContainer.scrollTo(0, xH);
}

// Function to add a new active user to the list
function addUser(user) {
  const userElement = document.createElement('div');
  userElement.classList.add('user');
  userElement.textContent =user;
  activeUsersContainer.appendChild(userElement);
}



// Event listener for receiving a new message
socket.on('message', message => {
  addMessage(message);
});


socket.on('connect', () => {
  socket.emit('join', { room: 'common_room' });
});


  

// Event listener for receiving an update to the active user list
socket.on('update active users', data => {
  activeUsersContainer.innerHTML = '';
  data.users.forEach(user => {
    addUser(user);
  });
});

socket.on('timed_out', data => {
  window.location.href = leaveUrl;
});

socket.on('history', function(data) {
for (let i = 0; i < data.messages.length; i++) {
addMessage(data.messages[i]);
}
});
