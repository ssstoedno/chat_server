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

//get client username
async function getUsername() {
    try {
      const response = await fetch('/get_username');
      const data = await response.json();
      return data.username;
    } catch (error) {
      console.error('Error getting username:', error);
    }
  }

// function to add a new message to the messages container
async function addMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    const username = await getUsername();
    console.log('New message:', message);
    const messageElement = document.createElement('div');
    if (message.username==username){
      messageElement.classList.add('my-message');
      messageElement.innerHTML = `<div class="badge bg-primary text-wrap" style="width: 35%;">
      <p class="text-break" style="font-size:1.1rem;" >You: ${message.message}</p>
      <small class="text-white">${new Date(message.time).toLocaleTimeString()}</small></div>`;
    }
    chatContainer.appendChild(messageElement);
    var xH = chatContainer.scrollHeight; 
    chatContainer.scrollTo(0, xH);
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
  