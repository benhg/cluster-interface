$(document).ready(function(){

$('#submit-button').click(function(){

    var fileData = new FormData($('#data')[0]);
    console.log(fileData);

    $.ajax({
        url:'http://mayo.blt.lclark.edu/webjobs/script',
        type: 'POST',
        data: fileData,
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
