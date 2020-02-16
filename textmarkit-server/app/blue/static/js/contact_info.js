
// Function to validate the form fields.
function validateForm() {
  var txtEmail = document.forms["submit_msg"]["txtEmail"].value;
  var txtMsg = document.forms["submit_msg"]["txtMsg"].value;

  if (txtEmail == "" && txtMsg == "") {
    alert("Email and message fields must be filled out");
    return false;
  }
  else if (txtMsg == ""){
    alert("Message field must be filled out");
    return false;
  }
  else if (txtEmail == ""){
    alert("Email must be filled out");
    return false;
  }

  if  (!( /(.+)@(.+){2,}\.(.+){2,}/.test(txtEmail))){
    // invalid email
    alert("Invalid email address. Please check for errors.");
    return false;
  }
}
