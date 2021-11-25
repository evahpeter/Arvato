

(function ($) {
    'use strict';

    /*[ File Input Config ]
        ===========================================================*/
    
    try {
		//alert('I am here');
       //var img = $('.loading');
	   var img = document.getElementById('loading');
	   img.style.visibility = 'hidden';
	   
	   var file_input_container = $('.js-input-file');
    
        if (file_input_container[0]) {
    
            file_input_container.each(function () {
    
                var that = $(this);
    
                var fileInput = that.find(".input-file");
                var info = that.find(".input-file__info");
    
                fileInput.on("change", function () {
    
                    var fileName;
                    fileName = $(this).val();
					var ext = fileName.substring(fileName.lastIndexOf('.') + 1);
					
					if (ext == 'csv')
					{
						if (fileName.substring(3,11) == 'fakepath') {
							fileName = fileName.substring(12);
						}
		
						if(fileName == "") {
							info.text("No file chosen");
						} else {
							info.text( fileName.replace(/^.*[\\\/]/, '') + ' ready for upload' );
							var x = $('.space_span2');
								x[0].innerHTML = "";
							var d = $('.download_link');
								d[0].innerHTML = "";
								
							//info.text("Processing " + fileName.replace(/^.*[\\\/]/, '') + ".......");
							//img.style.visibility = 'visible';
						}
					} 
					else 
					{
						//alert(ext);
						info.text('Invalid file selected. Please upload ONLY CSV file.');
					}
                })
    
            });
    
        }
    
    
    
    }
    catch (e) {
        console.log(e);
    }

})(jQuery);

function formSubmit() {
  //alert("The form was submitted");
	var img = document.getElementById('loading');
	   img.style.visibility = 'visible';
	//var filename = document.getElementById('file');  
	
	var fullPath = document.getElementById('file').value;
	if (fullPath) {
		var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
		var filename = fullPath.substring(startIndex);
		if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
			filename = filename.substring(1);
			displayText = "Processing " + filename + "......."
    }
    //alert(displayText);
	}
	
	var x = document.getElementsByClassName("input-file__info");
		x[0].innerHTML = displayText;
	
}

function resetform() {
	document.getElementById("appointment-form").reset();
	var img = document.getElementById('loading');
	   img.style.visibility = 'hidden';
	var x = document.getElementsByClassName("input-file__info");
		x[0].innerHTML = "No file chosen";
	
	var list = document.getElementsByClassName('space_span');
	var n;
	for (n = 0; n < list.length; ++n) {
		list[n].innerHTML=' ';
	}
	
	var list = document.getElementsByClassName('textarea--style-6');
	var n;
	for (n = 0; n < list.length; ++n) {
		list[n].innerHTML=' ';
	}
}