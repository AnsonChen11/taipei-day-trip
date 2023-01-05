let slideIndex = 1;

window.onload = async function(){
    url = location.pathname;
    await fetch("/api" + url)
    .then(res => res.json())
    .then(data => {
        const slideShow = document.querySelector(".slideShowContainer");
        const dot = document.querySelector(".dots");
        document.title = "台北一日遊 | " + data.data.name
        for(let i = 0; i < data.data.images.length; i++){
            const slideShowDiv = document.createElement("div");
            slideShowDiv.className = "slideShow fade";
            slideShow.appendChild(slideShowDiv)
            const spotImage = document.querySelectorAll(".slideShow");
            const spotImageImg = document.createElement("img");
            spotImageImg.src = data.data.images[i];
            spotImage[i].appendChild(spotImageImg);

            const dotSpan = document.createElement("span");
            dotSpan.className = "dot"
            dotSpan.setAttribute("dot_id", i)
            dot.appendChild(dotSpan)
        }
        
        const attraction = document.querySelector(".profile");
        const attractionDiv = document.createElement("div");
        attractionDiv.textContent = data.data.name;
        attractionDiv.className = "attraction";
        attraction.insertBefore(attractionDiv, attraction.children[0]);

        const category = document.querySelector(".profile");
        const categoryDiv = document.createElement("div");
        categoryDiv.textContent = data.data.category + " at " + data.data.mrt;
        categoryDiv.className = "category";
        category.insertBefore(categoryDiv, category.children[1]);

        const description = document.querySelector(".description");
        const descriptionSpan = document.createElement("span");
        descriptionSpan.textContent = data.data.description;
        description.appendChild(descriptionSpan);

        const address = document.querySelector(".infos_address");
        const addressSpan = document.createElement("span");
        addressSpan.className = "address";
        addressSpan.textContent = data.data.address;
        address.appendChild(addressSpan);

        const transportation = document.querySelector(".infos_transport");
        const transportationSpan = document.createElement("span");
        transportationSpan.className = "transportation";
        transportationSpan.textContent = data.data.transport;
        transportation.appendChild(transportationSpan);
        
        showSlides(slideIndex)
    })  
}

/* ------------------Option change price between morning or afternoon--------------------- */
const morning = document.querySelector(".morning")
const afternoon = document.querySelector(".afternoon")
const price = document.querySelector(".price")
morning.addEventListener("click", function(){
    price.textContent = "新台幣 2000 元";
})
afternoon.addEventListener("click", function(){
    price.textContent = "新台幣 2500 元";
})

/* ------------------click slides to change next or previous image--------------------- */
const previous = document.querySelector(".previous")
const next = document.querySelector(".next")
previous.addEventListener("click", function(){
    plusSlides(-1);
})
next.addEventListener("click", function(){
    plusSlides(1);
})
function plusSlides(n){
    showSlides(slideIndex += n);
}

/* ---------------------------click dot to slide image ----------------------------- */
document.addEventListener("click", function(e){
    const target = e.target.closest("[dot_id]");
    if(target){
        let dotId = parseInt(target.getAttribute('dot_id')) + 1
        currentSlide(dotId)
    }
});
/* ----------------------function of currentSlide & showSlides------------------------ */
function currentSlide(n){
    showSlides(slideIndex = n);
}

function showSlides(n){
    let i;
    const slideShow = document.querySelectorAll(".slideShow");
    const dot = document.querySelectorAll(".dot");
    if(n > slideShow.length){ //若index超過最後一張，回到第一張
        slideIndex = 1;
    }
    if(n < 1){ //若index超過第一張(小於1)，回到最後一張
        slideIndex = slideShow.length;
    }
    for(i = 0; i < slideShow.length; i++){
        slideShow[i].style.display = "none";
    }
    for(i = 0; i < dot.length; i++){
        dot[i].className = dot[i].className.replace(" active", "");
    }
    slideShow[slideIndex-1].style.display = "block";
    dot[slideIndex-1].className += " active";
}

/* ---------------------------click booking button to book ----------------------------- */
const btn = document.querySelector(".btn")
btn.addEventListener("click", function(){
    removeErrorMessage()
    if(document.cookie){
        let attractionId = location.pathname.slice(12,);
        let date = document.querySelector(".date").value;
        let time = document.querySelector("input[name='radio']:checked").value;
        let price = document.querySelector(".price").textContent.slice(4,8);
        if(attractionId && date && time && price){
            const url = "/api/booking";
            const headers = {
                "Content-Type": "application/json"
            };
            let body = {
                "attractionId": attractionId,
                "date": date,
                "time": time,
                "price": price,
            };
            fetch(url, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(response => response.json())
            .then(data => {
                if(data){
                    window.location.replace("/booking")
                }
            })
        }
        else{
            const dateDiv = document.querySelector(".dateDiv");
            const dateMessage = document.createElement("span");
            dateMessage.className = "loginErrorMessage";
            dateMessage.textContent = "請記得選擇日期！";
            dateDiv.appendChild(dateMessage)
        }
    }
    if(!document.cookie){
        overlay.style.display = "block";
        login.style.display = "block"
    }
})
/*--------------------function of remove error message--------------------*/
function removeErrorMessage(){
    const loginErrorMessage = document.querySelector(".loginErrorMessage")
    if(loginErrorMessage){
        loginErrorMessage.remove()
    }
}
/* ---------------------------datepicker only allow tomorrow onwards----------------------------- */
const date = document.querySelector('.date');

const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
date.min = tomorrow.toISOString().split('T')[0];