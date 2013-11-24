$(document).ready(function(){
    $("#mainform").submit(function(e){
	e.preventDefault();
	$.post("/generater/", $("#mainform").serialize(), function(data){
	    $("#message").html(data);
        });
    });

    $("#send").click(function(){	
        var config = {
	    'client_id': '978318033030-tjl927lvnr2p0n95put92jhkcbabt6to',
	    'scope': 'https://www.google.com/m8/feeds',
	    'apiKey' : 'AIzaSyANEFvTPo7SvqbmjlW6MtjDFByxBDjHSdE',
        };
	gapi.auth.authorize(config, function() {
	    console.log('login complete');
	    var authParams = gapi.auth.getToken();
	    authParams.alt = 'json';
	    
	    $.ajax({
		url: 'https://www.google.com/m8/feeds/contacts/default/full',
		dataType: 'json',
		data: authParams,
		success: function(data) {
		    var to_send = {
			form:$("#mainform").serialize(),
			gmail:data,
		    }
		    console.log(data);
		    $("#result").text(JSON.stringify(data));
		    $.ajax({
			url:"/create/",
			type:"POST",
			data:JSON.stringify(to_send),
			contentType:"application/json; charset=utf-8",
			dataType:"json",
			success: function(d, s, j){
			    console.log(d);
			    console.log(s);
			     window.location = "/page/?page="+d
			}
		    });

		}
	    });
        });
    });
});