const usernameField  =  document.querySelector('#usernameField');
const feedbackField = document.querySelector('.feedback');
const emailField = document.querySelector('#emailField'); 
const emailFeedback =  document.querySelector('.emailfeedback');
const usernameoutputField = document.querySelector('.usernameOutputField');
const  showpasword  =  document.querySelector('.showpasword'); 
const passwordField =  document.querySelector('#passwordField');
const submitBtn =  document.getElementById('submitbtn');
usernameField.addEventListener('keyup' , (e)=>{
    const  username =  e.target.value; 
    
    usernameoutputField.textContent=`Checking ${username} ? `; 
    usernameoutputField.style.display = 'block';
    usernameField.classList.remove('is-invalid');
    feedbackField.style.display = 'none';
    feedbackField.innerHTML = "";
    console.log(username);

    if (username.length > 0) {
        fetch('/authentication/validate-username'  ,  {
            body:JSON.stringify ({'username' :  username }) , 
            method: 'POST',
        }).then(res => res.json()).then(data =>{
            usernameoutputField.style.display = 'none';
            if (data.username_error){
                usernameField.classList.add('is-invalid');
                feedbackField.style.display = 'block';
                feedbackField.innerHTML+=`<p>${data.username_error}</p>`;
                submitBtn.disabled=  true;
            }else {
             submitBtn.disabled= false;
            }
        })
    }
})

// validate email
emailField.addEventListener('keyup' , (e)=>{
    const  email =  e.target.value;
    emailField.classList.remove('is-invalid');
    emailFeedback.style.display = 'none';
    emailFeedback.innerHTML = "";
    console.log(email);
    if (email.length > 0) {
        fetch('/authentication/validate-email'  ,  {
            body:JSON.stringify({"email":  email }) ,
            method: 'POST',
        }).then(res => res.json()).then(data =>{
            if (data.email_error){
                emailField.classList.add('is-invalid');
                emailFeedback.style.display = 'block';
                emailFeedback.innerHTML+=`<p>${data.email_error}</p>`;
                 submitBtn.disabled=  true;
            }else {
                submitBtn.disabled=  false;
            }

        })
    }
})

const   handleToggleInput=(e)=>{
    if (showpasword.textContent === "Show") {
        showpasword.textContent = "Hide" 
        passwordField.type = "text"
    } else{
        showpasword.textContent = "Show"
         passwordField.type = "password"

    }
}

showpasword.addEventListener('click' , handleToggleInput) 



