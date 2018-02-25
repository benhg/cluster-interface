$(document).ready(function(){

$('#submit-button').click(function(){

    var formData = new FormData($('#data')[0]);
    console.log(formData);

    $.ajax({
        url:'/register',
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {
            if(data!="pass"){
		$("h1").append("<h2 style='color:red'>"+data+"</h2>");
	    }else{
		window.location.replace('http://localhost:5000/newjob');
	    }
        },
        cache: false,
        contentType: false,
        processData: false
    });
    return false;
});
});
