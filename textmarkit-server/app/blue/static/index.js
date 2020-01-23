

// $('#call-to-action,.click-upload').click(function() {
//     $('#call-to-action').addClass('upload--loading');
//     $('.upload-hidden').click();
//   });
// $('.upload-hidden').change(function() {
//   $('#call-to-action').removeClass('upload--loading');
//   $('body').addClass('file-process-open');
// });
// $('.file-upload-bar-closed').click(function() {
//   $('body').removeClass('file-process-open');
// });
// $('.button open-contact').click(function() {
//   // $('body').toggleClass('file-process-open');
//   document.querySelector('#button open-contact').textContent = request.method;

// });

// $('#fileElem').change(function() {
//   var file = this.files[0].name;
//   ('file-upload-filename').text(file);
// });

// document.addEventListener('DOMContentLoaded', function() {
//   // do stuff here
//   let d = new Date();
//   document.getElementById('file-upload-filename').innerText = d;
// }, false);


$('#fileElem').on('change',function(){
  var fileName = $(this).val();
  document.getElementById('file-upload-filename').innerText = fileName;
});

// var input = document.getElementById('fileElem');
// var fileInfoArea = document.getElementById('file-upload-filename');

// document.addEventListener("DOMContentLoaded", displayFileName, false);
// // input.addEventListener('change', displayFileName);

// function displayFileName(event){
//   // fileInfoArea.textContent = "yes";
//   var file = event.srcElement;
//   var filename = input.files[0].name; 
//   console.log(filename);
//   fileInfoArea.textContent = 'File uploaded: ' + filename + ' Please verify that the uploaded file is either a digital pdf/txt.';
// };

// $('#fileElem').bind('change', function(){
//   var filename = $('#fileElem').val();
//   $('file-upload-filename').text(filename);
// });

  // $(function(evt) {
  //   evt.stopPropogation();
  //   evt.preventDefault();

  //   var file = evt.target.file();
    

    // var ul = $('#upload ul');
  
    // $('#drop a').click(function() {
    //   // Simulate a click on the file input button
    //   // to show the file browser dialog
    //   $(this).parent().find('input').click();
    // });
  
    // // Initialize the jQuery File Upload plugin
    // $('#upload').fileupload({
  
    //   // This element will accept file drag/drop uploading
    //   dropZone: $('#drop'),
  
    //   // This function is called when a file is added to the queue;
    //   // either via the browse button, or via drag/drop:
    //   add: function(e, data) {
  
    //     var tpl = $('<li class="working"><input type="text" value="0" data-width="48" data-height="48"' +
    //       ' data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');
  
    //     // Append the file name and file size
    //     tpl.find('p').text(data.files[0].name)
    //       .append('<i>' + formatFileSize(data.files[0].size) + '</i>');
  
    //     // Add the HTML to the UL element
    //     data.context = tpl.appendTo(ul);
  
    //     // Initialize the knob plugin
    //     tpl.find('input').knob();
  
    //     // Listen for clicks on the cancel icon
    //     tpl.find('span').click(function() {
  
    //       if (tpl.hasClass('working')) {
    //         jqXHR.abort();
    //       }
  
    //       tpl.fadeOut(function() {
    //         tpl.remove();
    //       });
  
        // });
  
//         // Automatically upload the file once it is added to the queue
//         var jqXHR = data.submit();
//       },
  
//       progress: function(e, data) {
  
//         // Calculate the completion percentage of the upload
//         var progress = parseInt(data.loaded / data.total * 100, 10);
  
//         // Update the hidden input field and trigger a change
//         // so that the jQuery knob plugin knows to update the dial
//         data.context.find('input').val(progress).change();
  
//         if (progress == 100) {
//           data.context.removeClass('working');
//         }
//       },
  
//       fail: function(e, data) {
//         // Something has gone wrong!
//         data.context.addClass('error');
//       }
  
//     });
  
    // Prevent the default action when a file is dropped on the window
    // $(document).on('drop dragover', function(e) {
    //   e.preventDefault();
    // });
  
//     // Helper function that formats the file sizes
//     function formatFileSize(bytes) {
//       if (typeof bytes !== 'number') {
//         return '';
//       }
  
//       if (bytes >= 1000000000) {
//         return (bytes / 1000000000).toFixed(2) + ' GB';
//       }
  
//       if (bytes >= 1000000) {
//         return (bytes / 1000000).toFixed(2) + ' MB';
//       }
  
//       return (bytes / 1000).toFixed(2) + ' KB';
//     }
  
//   });