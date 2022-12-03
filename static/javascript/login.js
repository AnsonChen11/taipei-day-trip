const closeBtnforlogin = document.querySelector(".closeBtnforlogin");
const closeBtnforsigin = document.querySelector(".closeBtnforsigin")
const login = document.querySelector(".login");
const signin = document.querySelector(".signin");
const item2 = document.querySelector(".item2")
const overlay = document.querySelector(".overlay")
const changeToLogin = document.querySelector(".changeToLogin")
const changeTosignin = document.querySelector(".changeTosignin")

item2.addEventListener("click", function(){
    login.style.display = "block"
    overlay.style.display = "block"
})

closeBtnforlogin.addEventListener("click", function(){
    login.style.display = "none"
    overlay.style.display = "none"
})

closeBtnforsigin.addEventListener("click", function(){
    signin.style.display = "none"
    overlay.style.display = "none"
})

changeToLogin.addEventListener("click", function(){
    login.style.display = "block"
    signin.style.display = "none"
})

changeTosignin.addEventListener("click", function(){
    login.style.display = "none"
    signin.style.display = "block"
})

overlay.addEventListener("click", function(){
    overlay.style.display = "none"
    signin.style.display = "none"
    login.style.display = "none"
})

