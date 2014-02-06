
window.onload = function(){
	localStorage.token = "";
	updateView();
};

function tabClick(selectTab, showPage, hidePages){


	document.getElementById(showPage).style.display = "block";
	document.getElementById('selectedTab').setAttribute("id", "");
	document.getElementsByName(selectTab)[0].setAttribute("id", "selectedTab");
	
	for (i = 0; i < hidePages.length; ++i) {
		
		document.getElementById(hidePages[i]).style.display = "none";
	}
}

function updateView(){

	if(localStorage.token == ""){
	
		alert('NOTsignedIn!');
		changeView('welcomeview');
	}
	else{
	
		//alert('signedIn!');
		changeView('signedinview');
	}
}

function catchSignInMessage(status){

	if(status.success){ 
	
		localStorage.token = status.data;
		updateView();
	}
	else{
	
		alert(status.message);
	}
}

function signIn(email, password){

	if(validSignIn(email, password)){
	
		catchSignInMessage(serverstub.signIn(email, password));
	}
	else{
	
		alert('Error');
	}
}

function signUp(input){		// {email, password, firstname, familyname, gender, city, country}

	if(validSignUp(input)){
	
		catchServerSignUpMessage(serverstub.signUp(input));
	}
}

//Validation

function validSignIn(email, password){

	return !(isEmpty(email) || isEmpty(password));
}

function validSignUp(input){	// {email, password, firstname, familyname, gender, city, country}

	var errorCount = 0;
 
	errorCount += validateField(['registerEmail'], [], isEmpty(input.email));
	errorCount += validateField(['registerPassword', 'registerPassword2'], ['registerPassword', 'registerPassword2'], isEmpty(input.password));
	errorCount += validateField(['registerPassword', 'registerPassword2'], ['registerPassword', 'registerPassword2'], isEmpty(input.passwordRep) || input.password != input.passwordRep);
	errorCount += validateField(['registerFirstName'], [], isEmpty(input.firstname));
	errorCount += validateField(['registerLastName'], [], isEmpty(input.familyname));
	errorCount += validateField(['registerGender'], [], isEmpty(input.gender));
	errorCount += validateField(['registerCountry'], [], isEmpty(input.country));
	errorCount += validateField(['registerCity'], [], isEmpty(input.city));
	
	return errorCount == 0;
}


function validateField(borderFieldIdArray, clearFieldIdArray, errorCondition){

	if(errorCondition){
	
		setFieldBorders(borderFieldIdArray, "thin solid red");
		clearFields(clearFieldIdArray);
	}
	else{
	
		setFieldBorders(borderFieldIdArray, "");
	}
	
	return errorCondition;
}

function catchServerSignUpMessage(msg){

	if(msg.success){
	
		clearFields(['registerEmail', 'registerPassword', 'registerPassword2', 'registerFirstName', 'registerLastName', 'registerGender', 'registerCountry', 'registerCity']);
		alert(msg.message);
	}
	else
	{
	
		if(msg.message == "User already exists."){

			document.getElementById('registerEmail').style.border="thin solid red";
			alert(msg.message); 
		}
	}
	
}

//Util

function setFieldBorders(fieldIdArray, borderStyle){

	for (i = 0; i < fieldIdArray.length; ++i) {
		
		document.getElementById(fieldIdArray[i]).style.border = borderStyle;
	}
}

function clearFields(fieldIdArray){

	for (i = 0; i < fieldIdArray.length; ++i) {
		
		document.getElementById(fieldIdArray[i]).value = "";
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


