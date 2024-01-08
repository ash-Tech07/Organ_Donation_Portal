// utility functions
function getCustomFormattedTime(date){
    let hours = date.getHours();
    let minutes = date.getMinutes();
    let mid='AM';
    if(hours==0){
        hours=12;
    }
    else if(hours>12){
        hours=hours%12;
        mid='PM';
    }

    return `${hours%13}:${minutes} ${mid}`
}

var chat_id = 0;
function get_chatbot_response_template(chatbot_response, chatbot_response_time, c_id){
    chat_id += 1;
    return `<li class='clearfix' id='${c_id}'> <div class='message-data text-right'> <span class='message-data-time'>${chatbot_response_time}</span> <img src='https://bootdey.com/img/Content/avatar/avatar1.png' alt='avatar'> </div> <div class='message other-message float-right'>${chatbot_response}</div> </li>`;
}



// chatbot initialization
var chatbot_initial_response = "Hi there! Shoot any kidney donation realted questions that you have.";
$(document).ready(function () {
    $(get_chatbot_response_template(chatbot_initial_response, getCustomFormattedTime(new Date($.now())), chat_id)).appendTo("#chat_history").hide().show('normal');
});


// chatbot response function 
var chatbot_error_response = "Hey we have run into some issuses! Please try again later.";
$("#chatbot_user_input").on('keyup', function (e) {
    if (e.key === 'Enter' || e.keyCode === 13) {
        let user_response = $("#chatbot_user_input").val();
        let user_response_time = getCustomFormattedTime(new Date($.now()));
        let user_response_template = `<li class='clearfix'> <div class='message-data'> <span class='message-data-time'>${user_response_time}</span> </div> <div class='message my-message'>${user_response}</div> </li>`;

        // add the new chat to chat history 
        $(user_response_template).appendTo("#chat_history").hide().show('normal');

        // make a post request to get the data 
        $.post('/chatbot', { user_response: user_response}, function (response, status) {
            if(status == 'success'){
                // add the chatbot response to chat history 
                $(get_chatbot_response_template(response, getCustomFormattedTime(new Date($.now())), chat_id)).appendTo("#chat_history").hide().show('normal');
            }else{
                // add the ERROR chatbot response to chat history 
                $(get_chatbot_response_template(chatbot_error_response, getCustomFormattedTime(new Date($.now())), chat_id)).appendTo("#chat_history").hide().show('normal');
            }
            
            $("#chat_container").animate({ scrollTop: $('#chat_container')[0].scrollHeight }, 800);
        });
        
        

    }
});