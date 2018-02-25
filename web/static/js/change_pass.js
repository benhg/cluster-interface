$(document).ready(function(){

$('#submit-button').click(function(){

    var formData = new FormData($('#data')[0]);
    console.log(formData);

    $.ajax({
        url:'/changepass',
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {
            if(data=="fail"){
		$("h1").append("<h2 style='color:red'>Invalid Username or Password</h2>");
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
