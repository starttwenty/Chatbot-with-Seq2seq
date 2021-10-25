let animateChatBot          = document.querySelector( ".chatBot" )
let animateChatSeparater    = document.querySelector( ".chatBot .chatBotHeading + hr" )
let animateChatBody         = document.querySelector( ".chatBot .chatBody" )
let animateChatForm         = document.querySelector( ".chatBot .chatForm" )
let chatOpenTrigger         = document.querySelector( ".chatBot .chatBotHeading #chatOpenTrigger" )
let chatCloseTrigger        = document.querySelector( ".chatBot .chatForm #chatCloseTrigger" )

chatOpenTrigger .addEventListener( "click" , openChatBot  )
chatCloseTrigger.addEventListener( "click" , closeChatBot )

let chatSession             = document.querySelector( ".chatBot .chatBody .chatSession" )

var chatBotIteration        = 0

//  // Function to open ChatBot
function openChatBot() {
    setTimeout(function(){
        //  // Animate ChatBot
        animateChatBot.classList.add( "active" )
    }, 0)
    setTimeout(function(){
        //  // Animate ChatOpenTrigger
        chatOpenTrigger.classList.add( "active" )
    }, 250)
    setTimeout(function(){
        //  // Animate ChatSeperater
        animateChatSeparater.classList.add( "active" )
    }, 500)
    setTimeout(function(){
        //  // Animate ChatBody
        animateChatBody.classList.add( "active" )
    }, 750)
    setTimeout(function(){
        //  // Animate ChatForm
        animateChatForm.classList.add( "active" )
    }, 1000)
    if( chatBotIteration == 0 )
        setTimeout(function(){
            //  // Initiate chat
            initiateConversation()
        }, 2000)
    chatBotIteration++
}

//  // Function to close ChatBot
function closeChatBot() {
    setTimeout(function() {
        //  // Animate ChatForm
        animateChatForm.classList.remove( "active" )
    }, 0)
    setTimeout(function() {
        //  // Animate ChatBody
        animateChatBody.classList.remove( "active" )
    }, 250)
    setTimeout(function() {
        //  // Animate ChatSeperater
        animateChatSeparater.classList.remove( "active" )
    }, 500)
    setTimeout(function() {
        //  // Animate ChatOpenTrigger
        chatOpenTrigger.classList.remove( "active" )
    }, 750)
    setTimeout(function() {
        //  // Animate ChatBot
        animateChatBot.classList.remove( "active" )
    }, 1000)
}