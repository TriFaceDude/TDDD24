
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

	if(myToken() == ""){
	
		changeView('welcomeview');
	}
	else{
	
		changeView('signedinview');
	}
}

function postMessage(msg){

	msg = serverstub.postMessage(myToken(), msg, 'g');
	updateWall();
}

function formatPosts(){
	
	msgArray = getMessages();
	posts = document.getElementsByClassName('wallPost');
	postCount = Math.min(posts.length, msgArray.length);
	
	for (i = 0; i < postCount; ++i) {
		
		posts[i].getElementsByClassName('postSender')[0].innerHTML = msgArray[i].writer;
		posts[i].getElementsByClassName('postContent')[0].innerHTML = msgArray[i].content;
	}
}

function updateWall(){

	clearWall();
	formatPosts();
}

function getMessages(){

	msg = serverstub.getUserMessagesByToken(myToken());
	
	if(msg.success){
	
		return msg.data;
	}
	else{
	
		alert('Failed retrive wall: ' + msg.message);
	}
}

function signIn(email, password){

	if(validSignIn(email, password)){
	
		catchSignInMessage(serverstub.signIn(email, password));
	}
	else{
	
		setLabelText('signInErrorLabel', 'Incomplete information.');
	}
}

function signUp(input){		// {email, password, firstname, familyname, gender, city, country}

	if(validSignUp(input)){
	
		catchServerSignUpMessage(serverstub.signUp(input));
	}
	else{
	
		setLabelText('registerErrorLabel', 'Incomplete information.');
	}
}

function changePassword(oldPassword, newPassword, newPasswordRepeat){


	if(validChangePassword(input)){
	
		catchServerChangePasswordMessage(serverstub.changePassword(myToken(), oldPassword, newPassword));
	}
}

function signOut(){

	serverstub.signOut(myToken());
	localStorage.token = "";
	updateView();
}

//##########
//Server message catching
//##########

function catchSignInMessage(msg){

	if(msg.success){ 
	
		localStorage.token = msg.data;
		updateView();
		updateWall();
	}
	else{
	
		setLabelText('signInErrorLabel', msg.message);
	}
}

function catchServerSignUpMessage(msg){

	if(msg.success){
	
		clearFields(['registerEmail', 'registerPassword', 'registerPassword2', 'registerFirstName', 'registerLastName', 'registerGender', 'registerCountry', 'registerCity']);
	}
	else
	{
	
		if(msg.message == "User already exists."){

			document.getElementById('registerEmail').style.border="thin solid red";
			setLabelText('registerErrorLabel', msg.message);
		}
	}
	
}

function catchServerChangePasswordMessage(msg){

	if(msg.success){
	
		setLabelText('changeErrorLabel', msg.message);
	}
	else{
	
		if(msg.message == "Wrong password."){
		
			setLabelText('changeErrorLabel', msg.message);
			validateField(['changeButton'], ['changeButton'], false)
		}
	}
}


//##########
//Validation
//##########

function validSignIn(email, password){

	return !(isEmpty(email) || isEmpty(password));
}

function validChangePassword(oldPassword, newPassword, newPasswordRepeat){

	var errorCount = 0;
 
	errorCount += validateField(['oldPassword'], [], isEmpty(oldPassword));
	errorCount += validateField(['newPassword', 'newPasswordRepeat'], ['newPassword', 'newPasswordRepeat'], isEmpty(newPassword));
	errorCount += validateField(['newPassword', 'newPasswordRepeat'], ['newPassword', 'newPasswordRepeat'], newPassword != newPasswordRepeat);
	
	return errorCount == 0;
}

function validSignUp(input){	// {email, password, firstname, familyname, gender, city, country}

	var errorCount = 0;
 
	errorCount += validateField(['registerEmail'], [], isEmpty(input.email));
	errorCount += validateField(['registerPassword', 'registerPassword2'], ['registerPassword', 'registerPassword2'], isEmpty(input.password));
	errorCount += validateField(['registerPassword', 'registerPassword2'], ['registerPassword', 'registerPassword2'], input.password != input.passwordRep);
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

//##########
//Util
//##########

function toArray(obj){

	return Array.prototype.slice.call(obj)
}

function elementArrayByName(name){

	return toArray(document.getElementsByName(name));
}

function myToken(){

	return localStorage.token;
}

function clearWall(){

	posts = elementArrayByName('wallPost');
	
	for (i = 0; i < posts.length; ++i) {
		
		posts[i].innerHTML = ""; 
	}
}

function setLabelText(labelId, text){

	document.getElementById(labelId).innerHTML = text;
}

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
