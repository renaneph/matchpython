function isGood(password, password_id, form_id) {
  var password_strength;

  if (form_id == undefined) {
    password_strength = document.querySelector("#" + password_id);
  } else {
    password_strength = document.querySelector("#" + form_id + " #" + password_id);
  }

  //TextBox left blank.
  if (password && password.length == 0) {
    password1_strength.innerHTML = "";
    return;
  }

  //Regular Expressions.
  var regex = new Array();
  regex.push("[A-Z]"); //Uppercase Alphabet.
  regex.push("[a-z]"); //Lowercase Alphabet.
  regex.push("[0-9]"); //Digit.
  regex.push("[$@$!%*#?&]"); //Special Character.

  var passed = 0;

  if (password.length >= 8) passed = 1;

  //Validate for each Regular Expression.
  for (var i = 0; i < regex.length; i++) {
    if (new RegExp(regex[i]).test(password)) {
      passed++;
    }
  }
  //Display status.
  var strength = "";
  switch (passed) {
    case 0:
    case 1:
    case 2:
      strength = "<small class='progress-bar bg-danger' style='width: 20%'>Weak</small>";
      break;
    case 3:
      strength = "<small class='progress-bar bg-warning' style='width: 40%'>Not yet</small>";
      break;
    case 4:
      strength = "<small class='progress-bar bg-info' style='width: 60%'>Medium</small>";
      break;
    case 5:
      strength = "<small class='progress-bar bg-success' style='width: 100%'>Strong</small>";
      break;

  }
  password_strength.innerHTML = strength;

  return passed == 5;

}

