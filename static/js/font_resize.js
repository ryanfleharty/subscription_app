function fontsize(){
    if($(window).width() < 551){
        var size = $('.nav_bar').width() * 0.05;
    } else {
        var size = $('.nav_bar').width() * 0.02;
    }
    $("button").css('font-size', size);
};
$(window).resize(fontsize);
$(document).ready(fontsize);
