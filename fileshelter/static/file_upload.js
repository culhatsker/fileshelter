(function () {
  var uploadForm = document.getElementById('uploadForm');
  var fileInput = document.getElementById('uploadFiles');
  
  uploadForm.addEventListener('submit', function (evnt) {
    evnt.preventDefault();
    for (let file of fileInput.files) {
      var formData = new FormData();
      var request = new XMLHttpRequest();
      formData.set('file', file);
      request.open('POST', uploadForm.action);
      request.send(formData);
    }
    fileList.forEach(function (file) {
    	sendFile(file);
    });
  });
})();