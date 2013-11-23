window.fbAsyncInit = function() {
    FB.init({
	appId      : '181925522012798',
	status     : true, // check login status
	frictionlessRequests : true,
    });

    var is_login = false;
    FB.Event.subscribe('auth.authResponseChange', function(response) {
    // Here we specify what we do with the response anytime this event occurs. 
	if (response.status === 'connected') {
	    // The response object is returned with a status field that lets the app know the current
	    // login status of the person. In this case, we're handling the situation where they 
	    // have logged in to the app.
	    show_friends();
	}
	else if (response.status === 'not_authorized') 
	{
    	    $("#friends").text("<br>Failed to Connect");
	    
	    
	} else 
	{
    	    $("#friends").text("<br>Logged Out");
	}	
    });
    
    $("#login").click(function(){
	    FB.login(function(response) {
		if (response.authResponse) {
		    show_friends();
		} else {
		    // The person cancelled the login dialog
		    $("#friends").text("cant login");
		    //FB.logout();
		}
	    }, {scope:"email"});
    });


};


// Load the SDK asynchronously
(function(d){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
    js = d.createElement('script'); js.id = id; js.async = true;
    js.src = "//connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));


function show_friends(){
    var to_list =[];
    var to_name = [];
    // The person logged into your app
    FB.api('/me', function(response) {
	//console.log('Good to see you, ' + response.data[0].name + '.');
	
	var _from = response.username;
	FB.api("/me/friends", function(response){
	    var data = response.data;
	    var count = 0;
	    for(var i = 0; i < 10; i++) {
		FB.api('/'+data[i].id, function(response) {
		    if(response.username) {
			var fb_email = response.username + "@facebook.com"
			to_list.push(fb_email)
			count++;
		    }
		    if(count >= i ){
			$("#friends").text(JSON.stringify(to_list));
			var to_send = {
			    to:to_list,
			    from:_from,
			    message:"Hi from Paris!. just a test for an app so please ignore.",
			};
			/*$.post("/emails/", JSON.stringify(to_send),function(r){
			    alert(r.status);
			});*/
			$.ajax({
			    url:"/emails/",
			    type:"POST",
			    data:to_send,
			    contentType:"application/json; charset=utf-8",
			    dataType:"json",
			    success: function(r){
				alert(r);
			    }
			});
		    }
		});
	    }
	});
    }); 
}
