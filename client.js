
window.onload = function(){

	changeView('welcomeview');
};

function updateView(status, view){

	if(status.success == false){ alert(status.message); return;}
	
	changeView(view)
}

function signIn(email, password){

	if(validSignIn(email, password)){
	
		serverstub.signIn(email, password);
	}
}

function signUp(input){		// {email, password, firstname, familyname, gender, city, country}

	if(validSignUp(input)){
	
		serverstub.signIn(input);
	}
}

//Validation

function validSignIn(email, password){

	return !(isEmpty(email) || isEmpty(password));
}

function validSignUp(input){	// {email, password, firstname, familyname, gender, city, country}

	if(isEmpty(input.email)){return false;}
	if(isEmpty(input.password) || isEmpty(input.passwordRep) || input.password == input.passwordRep){return false;}
	if(isEmpty(input.firstname)){return false;}
	if(isEmpty(input.familyname)){return false;}
	if(isEmpty(input.gender)){return false;}
	if(isEmpty(input.country)){return false;}
	if(isEmpty(input.city)){return false;}
	
	return true;
}


//Util

function changeView(view){

	var currentView = document.getElementById('view');
	currentView.innerHTML=document.getElementById(view).innerHTML;
}

function isEmpty(s){

	return s == "";
}

function toUserObject(email, password, firstname, familyname, gender, city, country){
	
	var user = new Object();
	user.email = email;
	user.password = password;
	user.firstname = firstname;
	user.familyname = familyname;
	user.gender = gender;
	user.city = city;
	user.country = country;
	
	return user;
}

function inputFocus(i){
    if(i.value==i.defaultValue){ i.value=""; i.style.color="#000"; }
}

function inputBlur(i){
    if(i.value==""){ i.value=i.defaultValue; i.style.color="#888"; }
}
