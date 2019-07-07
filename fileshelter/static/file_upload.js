(function () {
  var fileCatcher = document.getElementById('uploadForm');
  var fileInput = document.getElementById('uploadFiles');

  var directory = document.getElementById('upload-path')
  
  var fileList = [];
  var sendFile;
  
  fileCatcher.addEventListener('submit', function (evnt) {
  	evnt.preventDefault();
    fileList.forEach(function (file) {
    	sendFile(file);
    });
  });
  
  fileInput.addEventListener('change', function (evnt) {
 		fileList = [];
  	for (var i = 0; i < fileInput.files.length; i++) {
    	fileList.push(fileInput.files[i]);
    }
  });
  
  sendFile = function (file) {
  	var formData = new FormData();
    var request = new XMLHttpRequest();
 
    formData.set('file', file);
    request.open("POST", directory);
    request.send(formData);
  };
})();