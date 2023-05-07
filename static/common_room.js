async function getUsername() {
  try {
    const response = await fetch('/get_username');
    const data = await response.json();
    return data.username;
  } catch (error) {
    console.error('Error getting username:', error);
  }
}

// when client navigate away from page
 window.onbeforeunload = function() {
  socket.emit('leave');
  //window.location.href = leaveUrl;
  };

//prevent returning when logged out
function preventBack(){
  const queryParams = new URLSearchParams(window.location.search);
  const active = queryParams.get('active');
  if (active!='true'){
    window.history.forward();
  }
}
setTimeout("preventBack()", 0);
window.onunload=function(){null};

const socket = io.connect();
const messageForm = document.querySelector('#message-form');
const messageInput = document.querySelector('#message-input');
const messagesContainer = document.querySelector('#messages');
const activeUsersContainer = document.querySelector('#active-users .user-container');
const logoutLink = document.querySelector('#logout-button');

// message form event listener
messageForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  if (text) {
    socket.emit('message', { message: text });
    messageInput.value = '';
    messageInput.focus();
  }
});

// add message to message-container
async function addMessage(message) {
  const username = await getUsername();
  console.log('New message:', message);
  const messageElement = document.createElement('div');
  if (message.username==username){
    messageElement.classList.add('my-message');
    messageElement.innerHTML = `<div class="badge bg-primary text-wrap" style="width: 35%;">
    <p class="text-break" style="font-size:1.1rem;" >You: ${message.message}</p>
    <small class="text-white">${new Date(message.time).toLocaleTimeString()}</small></div>`;
  }
  else{
    messageElement.classList.add('message');
    messageElement.innerHTML = `<div class="badge bg-secondary text-wrap" style="width: 35%; margin-left:calc(65% - 25px)">
    <p class="text-break" style="font-size:1.1rem;" >${message.username}: ${message.message}</p>
    <small class="text-white" style="margin-left:calc(65% - 22px)">${new Date(message.time).toLocaleTimeString()}</small></div>`;
  }
  messagesContainer.appendChild(messageElement);
  var xH = messagesContainer.scrollHeight; 
  messagesContainer.scrollTo(0, xH);
}

$(document).ready(function() {
  // send a request to the server for messages since the last connection
  $.get('/messages', function(data) {
    // repopulate the message box with the new messages
    for (var i = 0; i < data.messages.length; i++) {
      addMessage({'username':data.messages[i][0],'message':data.messages[i][1], 'time':data.messages[i][2]});
    }
  });
});

// add active user
function addUser(user) {
  const userElement = document.createElement('div');
  userElement.classList.add('h6','user');
  userElement.textContent =user;
  activeUsersContainer.appendChild(userElement);
}

// Event listener connecting clients
socket.on('connect', () => {
  socket.emit('join', { room: 'common_room' });
});

// Event listener for receiving a new message
socket.on('message', message => {
  addMessage(message);
});

// Event listener for receiving an update to the active user list
socket.on('update active users', data => {
  activeUsersContainer.innerHTML = '';
  data.users.forEach(user => {
    addUser(user);
  });
});

// Event listener for session end
socket.on('timed_out', data => {
  window.location.href = leaveUrl;
});

