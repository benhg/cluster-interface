$(document).ready(function(){

$('#submit-button').click(function(){

    var formData = new FormData($('#data')[0]);

    $.ajax({
        url:'/script',
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {
            alert(data)
        },
        cache: false,
        contentType: false,
        processData: false
    });

    return false;
});
});
