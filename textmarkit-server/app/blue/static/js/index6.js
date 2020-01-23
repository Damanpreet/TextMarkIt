var extensions = ['pdf', 'txt', 'csv'];

function unlock(){
    document.getElementById('buttonsubmit').removeAttribute("disabled");
}

$('#upload_form').submit(function(event){
  validated = true;
  fname = document.getElementById('file-upload-filename').innerText;
  // if (extensions.includes(fname.split('.').pop())){
  if (extensions.includes(fname.substr(fname.lastIndexOf('.') + 1))){
    console.log("cool!")
  }
  else{
    validated = false;
    alert("Please upload pdf/txt file");
    // document.getElementById('file-upload-filename').innerText = "Please upload pdf/txt file";
      // Or some div with image showing
  }
  if (validated != true) {
      event.preventDefault();
  }
});

$('#fileElem').on('change',function(){
  var fileName = $(this).val();
  // fileName = fileName.split('\\');
  var ext = fileName.substr(fileName.lastIndexOf('.') + 1);
  // var fname = fileName[fileName.length-1];
  // if (extensions.includes(fname.split('.').pop())){
  if (extensions.includes(ext)){
    document.getElementById('file-upload-filename').innerText = fileName;//.split('\\').pop().split('/').pop();
  }
  else{
    document.getElementById('file-upload-filename').innerText = "Please upload pdf/txt file";
  }
});

