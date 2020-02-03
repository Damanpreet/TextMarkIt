var extensions = ['pdf', 'txt', 'csv'];

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
    alert("Please upload pdf/txt file");
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
  }
  else{
    document.getElementById('file-upload-filename').innerText = "Please upload pdf/txt file";
  }
});