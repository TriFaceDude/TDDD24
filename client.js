window.onload = function(){

	var currentView = document.getElementById('view');
	currentView.innerHTML=document.getElementById('welcomeview').innerHTML;
};

function inputFocus(i){
    if(i.value==i.defaultValue){ i.value=""; i.style.color="#000"; }
}

function inputBlur(i){
    if(i.value==""){ i.value=i.defaultValue; i.style.color="#888"; }
}

function validateSignIn(input){

	return !(isEmpty(input.username) || isEmpty(input.password));
}

function validateSignUp(input){

	if(isEmpty(input.username)){return false;}
	
}

function isEmpty(s){

	return s == "";
}

function changeView(view){

	var currentView = document.getElementById('view');
	currentView.innerHTML=document.getElementById(view).innerHTML;
}

function checkViewChange(status, view){

	if(status.success == false){ alert(status.message); return;}
	
	changeView(view)
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
