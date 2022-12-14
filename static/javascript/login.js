//for login and signup card
const login = document.querySelector(".login");
const signin = document.querySelector(".signin");
const overlay = document.querySelector(".overlay")

//click overlay disappear login or signup card
overlay.addEventListener("click", function(){
    overlay.style.display = "none";
    signin.style.display = "none";
    login.style.display = "none"
})


//for auth_booking
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


//for nav bar
const auth_login = document.querySelector(".auth_login")
const auth_logout = document.querySelector(".auth_logout")


//onload to check user login or not
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
        if(data.ok == true){
            location.reload()
        }
    })
})

//close button for login or signin 
const closeBtnforlogin = document.querySelector(".closeBtnforlogin");
const closeBtnforsigin = document.querySelector(".closeBtnforsigin");
closeBtnforlogin.addEventListener("click", function(){
    login.style.display = "none";
    overlay.style.display = "none"
})

closeBtnforsigin.addEventListener("click", function(){
    signin.style.display = "none";
    overlay.style.display = "none"
})

//change to login or change to signin card
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

//Signin or login's submit button
const submitForSignin = document.querySelector(".submitForSignin");
submitForSignin.addEventListener("click", function(e){
    e.preventDefault()
    const url = "/api/user";
    const headers = {
        "Content-Type": "application/json"
    };
    const body = {
        "name": document.getElementById("signinUsername").value,
        "email": document.getElementById("signinEmail").value,
        "password": document.getElementById("signinPassword").value
    };
    fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        const signinCard = document.querySelector(".signinCard");
        const signinCardDiv = document.createElement("div");
        if(data.ok == true){
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
})

const submitForLogin = document.querySelector(".submitForLogin")
submitForLogin.addEventListener("click", function(e){
    e.preventDefault()
    const url = "/api/user/auth"
    const headers = {
        "Content-Type": "application/json"
    }
    let body = {
        "email": document.getElementById("loginEmail").value,
        "password": document.getElementById("loginPassword").value
    }
    const loginCard = document.querySelector(".loginCard");
    const loginCardDiv = document.createElement("div");
    // if(body.email == "" | body.password == ""){
    //     loginCardDiv.className = "loginErrorMessage"
    //     loginCardDiv.textContent = "請輸入電子信箱或密碼";
    //     loginCard.insertBefore(loginCardDiv, changeToSignin);
    // }
    fetch(url, {
        method: "PUT",
        headers: headers,
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if(data.ok == true){
            loginCardDiv.className = "loginSuccessfulMessage"
            loginCardDiv.textContent = "登入成功";
            loginCard.insertBefore(loginCardDiv, changeToSignin);
            location.reload()
        }
        else{
            loginCardDiv.className = "loginErrorMessage"
            loginCardDiv.textContent = "登入失敗，電子信箱或密碼輸入錯誤";
            loginCard.insertBefore(loginCardDiv, changeToSignin);
            login.addEventListener("click", function(){
                loginCardDiv.style.display = "none"
            })
            closeBtnforlogin.addEventListener("click", function(){
                document.getElementById("loginForm").reset();
            })
            overlay.addEventListener("click", function(){
                document.getElementById("loginForm").reset();
            })
        }
    })
})