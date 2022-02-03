Dropzone.autoDiscover = false;
var myDropzone = new Dropzone('#my-awesome-dropzone', {       
    paramName: "file", 
    maxFilesize: 3.0, 
    maxFiles: 4,
    parallelUploads: 10000,
	dictDefaultMessage: "Drag file 70A_* or 70B_* or user_*",
    acceptedFiles : ".csv",
    uploadMultiple: true,
    autoProcessQueue: false,
    init: function() {
    	$("#loading").removeAttr("hidden")
		$("#loading").hide();
		var myDropzone = this;  
		$(document).on("click", '#btn-upload-file', function(event){
			 $("#loading").show();
			 event.preventDefault();
			 myDropzone.processQueue();
		 });
		  this.on('successmultiple', function(file, response) {
			  setTimeout(function(){
				  dt = JSON.parse(response);
				   filename=dt["file_name"];
				   uriContent = "data:application/octet-stream;base64," + encodeURIComponent(dt["data"]);
				   $('<a href="' + uriContent + '" download="' + filename + '" ></a>')[0].click();
				    $("#loading").hide();
				    myDropzone.removeAllFiles();  
			  }, 3000);
	        });
    }


    
});

function str2bytes (str) {
    var bytes = new Uint8Array(str.length);
    for (var i=0; i<str.length; i++) {
        bytes[i] = str.charCodeAt(i);
    }
    return bytes;
}
