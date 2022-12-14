//for login and signup card
const login = document.querySelector(".login");
const signin = document.querySelector(".signin");
const overlay = document.querySelector(".overlay")

/*----------------click overlay disappear login or signup card----------------*/
overlay.addEventListener("click", function(){
    overlay.style.display = "none";
    signin.style.display = "none";
    login.style.display = "none"
    removeErrorMessage()
})


/*------------------------------for auth_booking------------------------------*/
const auth_booking = document.querySelector(".auth_booking")
auth_booking.addEventListener("click", function(){
    if(document.cookie){
        location.href="/booking"
    }
    else{
        overlay.style.display = "block";
        login.style.display = "block"
    }
})


/*------------------------------for nav bar------------------------------*/
const auth_login = document.querySelector(".auth_login")
const auth_logout = document.querySelector(".auth_logout")


/*------------------------onload to check user login or not-------------------*/
fetch("/api/user/auth")
.then(response => response.json())
.then(data => {
    if(data.data === null){
        auth_login.style.display = "block"
    }
    else{
        auth_login.style.display = "none"
        auth_logout.style.display = "block"
    }
})

auth_login.addEventListener("click", function(){
    login.style.display = "block"
    overlay.style.display = "block"
})

auth_logout.addEventListener("click", function(){
    const url = "/api/user/auth"
    const headers = {
        "Content-Type": "application/json"
    }
    fetch(url, {
        method: "DELETE",
        headers: headers,
    })
    .then(response => response.json())
    .then(data => {
        if(data){
            location.reload()
        }
    })
})

/*--------------------close button for login or signin--------------------*/
const closeBtnforlogin = document.querySelector(".closeBtnforlogin");
const closeBtnforsigin = document.querySelector(".closeBtnforsigin");
closeBtnforlogin.addEventListener("click", function(){
    login.style.display = "none";
    overlay.style.display = "none";
    removeErrorMessage();
})

closeBtnforsigin.addEventListener("click", function(){
    signin.style.display = "none";
    overlay.style.display = "none";
    removeErrorMessage();
})

/*----------------change to login or change to signin card----------------*/
const changeToLogin = document.querySelector(".changeToLogin");
const changeToSignin = document.querySelector(".changeToSignin");
changeToLogin.addEventListener("click", function(){
    login.style.display = "block";
    signin.style.display = "none"
})

changeToSignin.addEventListener("click", function(){
    login.style.display = "none";
    signin.style.display = "block"
})

/*------------------------Signin submit------------------------*/
const submitForSignin = document.querySelector(".submitForSignin");
submitForSignin.addEventListener("click", function(e){
    e.preventDefault()
    removeErrorMessage()
    const signinCard = document.querySelector(".signinCard");
    const signinCardDiv = document.createElement("div");
    const url = "/api/user";
    const headers = {
        "Content-Type": "application/json"
    };
    const body = {
        "name": document.getElementById("signinUsername").value,
        "email": document.getElementById("signinEmail").value,
        "password": document.getElementById("signinPassword").value
    };
    if(body.name == "" | body.email == "" | body.password == ""){
        signinCardDiv.className = "loginErrorMessage";
        signinCardDiv.textContent = "請確認欄位皆已輸入";
        signinCard.insertBefore(signinCardDiv, changeToLogin);
    }
    else if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(body.email) === false){
        signinCardDiv.className = "loginErrorMessage";
        signinCardDiv.textContent = "email格式錯誤";
        signinCard.insertBefore(signinCardDiv, changeToLogin);
        // const signinEmail = document.getElementById("signinEmail")
        // signinEmail.style.borderColor = "red"
        // signinEmail.style.borderWidth = "medium"
    }
    else{
        fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            if(data){
                signinCardDiv.className = "loginSuccessfulMessage";
                signinCardDiv.textContent = "註冊成功，請登入系統";
                signinCard.insertBefore(signinCardDiv, changeToLogin);
                location.reload()
            }
            else{
                signinCardDiv.className = "loginErrorMessage";
                signinCardDiv.textContent = "註冊失敗，電子信箱已被註冊";
                signinCard.insertBefore(signinCardDiv, changeToLogin);
                signin.addEventListener("click", function(){
                    signinCardDiv.style.display = "none"
                });
                closeBtnforsigin.addEventListener("click", function(){
                    document.getElementById("signinForm").reset();
                });
                overlay.addEventListener("click", function(){
                    document.getElementById("signinForm").reset();
                })
            }
        })
    }
})
/*------------------------Login submit------------------------*/
const submitForLogin = document.querySelector(".submitForLogin")
submitForLogin.addEventListener("click", function(e){
    e.preventDefault();
    removeErrorMessage();
    const loginCard = document.querySelector(".loginCard");
    const loginCardDiv = document.createElement("div");
    const url = "/api/user/auth";
    const headers = {
        "Content-Type": "application/json"
    };
    let body = {
        "email": document.getElementById("loginEmail").value,
        "password": document.getElementById("loginPassword").value
    };
    if(body.email == "" | body.password == ""){
        loginCardDiv.className = "loginErrorMessage";
        loginCardDiv.textContent = "請確認欄位皆已輸入";
        loginCard.insertBefore(loginCardDiv, changeToSignin);
    }
    else if(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(body.email) === false){
        loginCardDiv.className = "loginErrorMessage";
        loginCardDiv.textContent = "email格式錯誤";
        loginCard.insertBefore(loginCardDiv, changeToSignin);
        // const loginEmail = document.getElementById("loginEmail")
        // loginEmail.style.borderColor = "red"
        // loginEmail.style.borderWidth = "medium"
    }
    else{
        fetch(url, {
            method: "PUT",
            headers: headers,
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            if(data.ok){
                loginCardDiv.className = "loginSuccessfulMessage";
                loginCardDiv.textContent = "登入成功";
                loginCard.insertBefore(loginCardDiv, changeToSignin);
                location.reload();
            }
            else{
                loginCardDiv.className = "loginErrorMessage";
                loginCardDiv.textContent = "登入失敗，電子信箱或密碼輸入錯誤";
                loginCard.insertBefore(loginCardDiv, changeToSignin);
                login.addEventListener("click", function(){
                    loginCardDiv.style.display = "none";
                });
                closeBtnforlogin.addEventListener("click", function(){
                    document.getElementById("loginForm").reset();
                });
                overlay.addEventListener("click", function(){
                    document.getElementById("loginForm").reset();
                });
            }
        })
    }
})

/*--------------------input addEventListener of remove error message--------------------*/
const formEmailInput = document.getElementById("loginEmail")
formEmailInput.addEventListener("click", function(){
    removeErrorMessage()
})
const formPasswordInput = document.getElementById("loginPassword")
formPasswordInput.addEventListener("click", function(){
    removeErrorMessage()
})
const signinUsername = document.getElementById("signinUsername")
signinUsername.addEventListener("click", function(){
    removeErrorMessage()
})
const signinEmail = document.getElementById("signinEmail")
signinEmail.addEventListener("click", function(){
    removeErrorMessage()
})
const signinPassword = document.getElementById("signinPassword")
signinPassword.addEventListener("click", function(){
    removeErrorMessage()
})

/*--------------------function of remove error message--------------------*/
function removeErrorMessage(){
    const loginErrorMessage = document.querySelector(".loginErrorMessage")
    if(loginErrorMessage){
        loginErrorMessage.remove()
    }
}



// const inputs = document.querySelectorAll("input")
// inputs.forEach(input => {
//     input.addEventListener("input", function(){
//         if(input.checkValidity()){
//             input.classList.add("valid")
//             input.classList.remove("invalid")
//         }
//         else{
//             input.classList.remove("valid")
//             input.classList.add("invalid")
//         }
//     })
// })
