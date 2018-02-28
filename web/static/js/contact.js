$(document).ready(function(){

$('#submit-button').click(function(){

    var formData = new FormData($('#data')[0]);
    console.log(formData);

    $.ajax({
        url:'http://mayo.blt.lclark.edu/webjobs/contact',
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {
            alert("Your message has been sent. Thanks for the feedback!")
        },
        cache: false,
        contentType: false,
        processData: false
    });
    return false;
});
});
