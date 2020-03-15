speedAnimationsSlow = 1000;
speedAnimationsQuick = 250;
timeWaiting = 5000

$(document).ready(function(){
    $("#add_server_button").on("click", function(){
        $("#add_server_layout").toggle(speedAnimationsQuick);
    });

    showNotification();
});

async function showNotification(){
    if(notification_type != 0){
        $("#active_notification").fadeIn(speedAnimationsSlow);
        await quitNotification(5000);
    }
}

function quitNotification(time) {
    return new Promise(resolve => {
        setTimeout(() => {
             $("#active_notification").fadeOut(speedAnimationsSlow);
        }, time);
    });
}