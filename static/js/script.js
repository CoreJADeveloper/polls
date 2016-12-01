jQuery(document).ready(function($){
	$('.poll-form').on('submit', function(event){
	    event.preventDefault();
	    $('#loading-ajax').removeClass('hide')
	    console.log("form submitted!");  // sanity check
	    var form_id = $(this).attr('id');
	    insert_vote(form_id);
	});

	function insert_vote(form_id){
		var form_id = form_id;
		$.ajax({
	        url : "/", 
	        type : "POST", 
	        data : $('#'+form_id).serialize(), 

	        success : function(data_object) {
	        	// console.log(data_object)
	        	$('#loading-ajax').addClass('hide')
	            if (data_object == 'Success') {
	            	$('#success-message').removeClass('hide');
	            }
	            else if (data_object == 'Exists') {
	            	$('#danger-message').removeClass('hide');
	            }
	            else if (data_object == 'User not authenticated') {
	            	$('#warning-message').removeClass('hide');
	            }
	            else if (data_object == 'Select option') {
	            	$('#select-choice-message').removeClass('hide');
	            }
	        },

	        error : function(xhr,errmsg,err) {
	            console.log(xhr.status + ": " + xhr.responseText); 
	        }
	    });
	}
})

