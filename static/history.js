async function getUsername() {
    try {
      const response = await fetch('/get_username');
      const data = await response.json();
      return data.username;
    } catch (error) {
      console.error('Error getting username:', error);
    }
  }
  
  window.onbeforeunload = function() {
      window.location.href = backUrl;
    }


// Function to add a new message to the messages container
async function addMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    const username = await getUsername();
    console.log('New message:', message);
    const messageElement = document.createElement('div');
    if (message.username==username){
      messageElement.classList.add('my-message');
      /*messageElement.innerHTML = `<div class="badge bg-primary text-wrap" style="width: 100;">
      <p class="text-break" style="font-size:1.1rem;" >You:${message.message}</p></div>`;*/
      messageElement.innerHTML = `<div class="badge bg-primary text-wrap" style="width: 35%;">
      <p class="text-break" style="font-size:1.1rem;" >You: ${message.message}</p>
      <small class="text-muted">${new Date(message.time).toLocaleTimeString()}</small></div>`;
    }
    /*
    else{
      messageElement.classList.add('message');
      messageElement.innerHTML = `<div class="badge bg-secondary text-wrap" style="width: 35%; margin-left:calc(65% - 25px)">
      <p class="text-break" style="font-size:1.1rem;" >${message.username}: ${message.message}</p>
      <small class="text-muted" style="margin-left:calc(65% - 25px)">${new Date(message.time).toLocaleTimeString()}</small></div>`;
    }
    
    const timeElement = document.createElement('small');
    timeElement.innerText = new Date(message.time).toLocaleTimeString(); // use the 'time' property of the message object to display the time
    timeElement.classList.add('text-muted');
    messageElement.appendChild(timeElement);*/
  
    chatContainer.appendChild(messageElement);
    var xH = chatContainer.scrollHeight; 
    chatContainer.scrollTo(0, xH);
  }


  $(document).ready(function() {
    // Send a request to the server for messages since the last connection
    $.get('/messages', function(data) {
      // Repopulate the message box with the new messages
      for (var i = 0; i < data.messages.length; i++) {
        addMessage({'username':data.messages[i][0],'message':data.messages[i][1], 'time':data.messages[i][2]});
      }
    });
  });
  