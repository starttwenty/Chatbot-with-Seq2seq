var chatBotSession              = document.querySelector( ".chatBot .chatBody .chatSession" )
var chatBotSendButton           = document.querySelector( ".chatBot .chatForm #sendButton" )
var chatBotTextArea             = document.querySelector( ".chatBot .chatForm #chatTextBox" )

var chatBotInitiateMessage      = "Hello! I am ChatBot."
var chatBotBlankMessageReply    = "Type something!"
var chatBotReply                = ""

var inputMessage                = ""

var typeOfContainer             = ""

chatBotSendButton.addEventListener("click", (event)=> {
    chatBotSession.scrollTop = chatBotSession.scrollHeight
    console.log("Before height: " + chatBotSession.scrollHeight)
    event.preventDefault()
    if( validateMessage() ){
        inputMessage    = chatBotTextArea.value
        typeOfContainer = "message"
        createContainer( typeOfContainer )
        typeOfContainer = "reply"
        createContainer( typeOfContainer )
    }
    else{        
        typeOfContainer = "error";
        createContainer( typeOfContainer )
    }
    chatBotTextArea.value = ""
    chatBotTextArea.focus()
})

async function sendPost(input) {
    const raw = await fetch('/test', {
    method: 'POST',
    headers: {'Content-type': 'application/json'},
    body: JSON.stringify({message: input })
    }).catch((error) => {
        console.log('Error send request');
        console.log(error);
    });
    const response = await raw.json()
    return response.reply
}

async function createContainer( typeOfContainer ) {
    var containerID = ""
    var textClass   = ""
    switch( typeOfContainer ) {
        case "message"      :
            containerID = "messageContainer"
            textClass   = "message"
            break;
        case "reply"        :
        case "initialize"   :
        case "error"        :
            containerID = "replyContainer"
            textClass   = "reply"
            break;
        default :
            alert("Error! Please reload the webiste.")
    }

    var newContainer = document.createElement( "div" )
    newContainer.setAttribute( "class" , "container" )
    if( containerID == "messageContainer" )
        newContainer.setAttribute( "id" , "messageContainer" )
    if( containerID == "replyContainer" )
        newContainer.setAttribute( "id" , "replyContainer" )
    chatBotSession.appendChild( newContainer )

    switch( textClass ) {
        case "message"  :
            var allMessageContainers    = document.querySelectorAll("#messageContainer")
            var lastMessageContainer    = allMessageContainers[ allMessageContainers.length - 1 ]
            var newMessage              = document.createElement( "p" )
            newMessage.setAttribute( "class" , "message animateChat" )
            newMessage.innerHTML        = escapeHtml(inputMessage)
            lastMessageContainer.appendChild( newMessage )
            setTimeout(function() {
                console.log("Message Height: " + chatBotSession.scrollHeight)
                chatBotSession.scrollTop = chatBotSession.scrollHeight
            }, 200)
            break
        case "reply"    :
            var allReplyContainers      = document.querySelectorAll( "#replyContainer" )    
            var lastReplyContainer      = allReplyContainers[ allReplyContainers.length - 1 ]
            var newReply                = document.createElement( "p" )
            newReply.setAttribute( "class" , "reply animateChat accentColor" )
            switch( typeOfContainer ){
                case "reply"        :
                    response = await sendPost(inputMessage)
                    chatBotReply = response
                    chatBotReply = escapeHtml(chatBotReply)
                    newReply.innerHTML  = chatBotReply
                    break
                case "initialize"   :
                    newReply.innerHTML  = chatBotInitiateMessage
                    break
                case "error"        :
                    newReply.innerHTML  = chatBotBlankMessageReply
                    break
                default             :
                    newReply.innerHTML  = "Sorry! I could not understannd."
            }
            lastReplyContainer.appendChild( newReply )
            setTimeout(function() {
                console.log("Reply Height: " + chatBotSession.scrollHeight)
                chatBotSession.scrollTop = chatBotSession.scrollHeight
            }, 230)
            break
        default         :
            console.log("Error in conversation")
    }
}

function initiateConversation() {
    chatBotSession.innerHTML = ""
    typeOfContainer = "initialize"
    createContainer( typeOfContainer )
}

function escapeHtml(str)
{
    var map =
    {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return str.replace(/[&<>"']/g, function(m) {return map[m];});
}