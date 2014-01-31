
window.onload = function(){

	changeView('welcomeview');
};

function updateView(status, view){

	if(status.success == false){ alert(status.message); return;}
	
	changeView(view)
}

function signIn(email, password){

	if(validSignIn(email, password)){
	
		updateView(serverstub.signIn(email, password), 'signedinview');
	}
	else{
	
		alert('Error');
	}
}

function signUp(input){		// {email, password, firstname, familyname, gender, city, country}

	if(validSignUp(input)){
	
		serverstub.signUp(input);
	}
	else{
	
		alert('Error');
	}
}

//Validation

function validSignIn(email, password){

	return !(isEmpty(email) || isEmpty(password));
}

function validSignUp(input){	// {email, password, firstname, familyname, gender, city, country}

	var signUpError = false;

	if(isEmpty(input.email)){changeInputBoxBorder('registerEmail', true); signUpError = true;}
	if(isEmpty(input.password)){changeInputBoxBorder('registerPassword', true); signUpError = true;}
	if(isEmpty(input.passwordRep) || input.password == input.passwordRep){changeInputBoxBorder('registerPassword2', true); signUpError = true;}
	if(isEmpty(input.firstname)){changeInputBoxBorder('registerFirstName', true); signUpError = true;}
	if(isEmpty(input.familyname)){changeInputBoxBorder('registerLastName', true); signUpError = true;}
	if(isEmpty(input.gender)){changeInputBoxBorder('registerGender', true); signUpError = true;}
	if(isEmpty(input.country)){changeInputBoxBorder('registerCountry', true); signUpError = true;}
	if(isEmpty(input.city)){changeInputBoxBorder('registerCity', true); signUpError = true;}
	
	return !signUpError;
}


//Util

function changeInputBoxBorder(boxID, setRed){

	if(setRed){
	
		document.getElementById(boxID).style.border="thin solid red";
	}
	else{
	
		document.getElementById(boxID).style.border="";
	}
}

function changeView(view){

	var currentView = document.getElementById('view');
	currentView.innerHTML=document.getElementById(view).innerHTML;
}

function isEmpty(s){

	return s == "";
}

function toUserObject(email, password, passwordRepeat, firstname, familyname, gender, city, country){
	
	var user = new Object();
	user.email = email;
	user.password = password;
	user.passwordRep = passwordRepeat;
	user.firstname = firstname;
	user.familyname = familyname;
	user.gender = gender;
	user.city = city;
	user.country = country;
	
	return user;
}

function inputBlur(i){
    if(i.value==""){ i.value=i.defaultValue; i.style.color="#888"; }
}

function inputFocus(i){
    if(i.value==i.defaultValue){ i.value=""; i.style.color="#000"; }
}
