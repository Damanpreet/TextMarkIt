var extensions = ['html', 'txt'];

function unlock(){
    document.getElementById('buttonsubmit').removeAttribute("disabled");
}

$('#upload_form').submit(function(event){
  validated = true;
  fname = document.getElementById('file-upload-filename').innerText;
  // if (extensions.includes(fname.split('.').pop())){
  if (extensions.includes(fname.substr(fname.lastIndexOf('.') + 1))){
    console.log("cool! correct file.");
    $('#loading-image').show();
  }
  else{
    validated = false;
    alert("Please upload html/txt file");
  }
  if (validated != true) {
      event.preventDefault();
  }
});

$('#fileElem').on('change',function(){
  var fileName = $(this).val();
  var ext = fileName.substr(fileName.lastIndexOf('.') + 1);
  
  if (extensions.includes(ext)){
    document.getElementById('file-upload-filename').innerText = fileName;//.split('\\').pop().split('/').pop();
    document.getElementById('file-upload-btn').disabled = false;
  }
  else{
    document.getElementById('file-upload-filename').innerText = "Please upload html/txt file";
    document.getElementById('file-upload-btn').disabled = true;
  }
});

// Functions to handle the drag and drop of the file, and send the file to the server.
var dragHandler = function(event){
  // Prevent the default action to open the file in the browser.
  event.preventDefault();
}

var dropHandler = function(event){
  event.preventDefault(); // Prevent the default action.

  // Create the form data.
  var files = event.originalEvent.dataTransfer.files;

  // Set the file in fileElem.
  fileElem.files = files;

  // Display the file name.
  var fileName = files[0].name;
  var ext = fileName.substr(fileName.lastIndexOf('.') + 1);
  if (extensions.includes(ext)){
    document.getElementById('file-upload-filename').innerText = fileName;
  }
  else{
    document.getElementById('file-upload-filename').innerText = "Please upload html/txt file";
  }
}

var dropHandlerSet = {
  dragover: dragHandler,
  drop: dropHandler
}

$(".upload").on(dropHandlerSet);

window.addEventListener("dragover", function(event){
  event.preventDefault();
}, false);

window.addEventListener("drop", function(event){
  event.preventDefault();
}, false);