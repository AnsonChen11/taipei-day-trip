/* ---------------------------change title name----------------------------- */
document.title = "台北一日遊 | 我的預定"
/* ---------------fetch api to confirm user is login or not ---------------- */
fetchApiBooking()
function fetchApiBooking(){
    fetch("/api/booking")
    .then(response => response.json())
    .then(data => {
        if(data.message == "未登入系統"){
            location.href="/";
        }
        if(data.data === null){
            const main = document.querySelector("main");
            const booking_view = document.querySelector(".booking_view");
            main.removeChild(booking_view);
            const booking_subtitle = document.createElement("div");
            booking_subtitle.className = "booking_subtitle";
            booking_subtitle.textContent = "您好，" + userData.name + "，待預訂的行程如下：";
            const noOrderDiv = document.createElement("div");
            noOrderDiv.className = "noOrderItem";
            noOrderDiv.textContent = "目前無任何預定";
            main.append(booking_subtitle, noOrderDiv);
        }
        else{
            createElementForBooking(data)
            getBookingData(data)
        }
    })
}
/* ---------------create Booking and details and count total price---------------- */
function createElementForBooking(data){
    let ttl_price = 0
    const booking_overall = document.querySelector(".booking_overall");
    data.data.forEach((e) =>{
        const booking_overview_sectionDIV = document.createElement("div");
        booking_overview_sectionDIV.className = "booking_overview_section"
/* -------------------------------------------------------------------------------- */
        const booking_imageDIV = document.createElement("div");
        booking_imageDIV.className = "booking_image";
        const booking_imageImg = document.createElement("img");
        booking_imageImg.src = e.attraction.image;
        booking_imageDIV.appendChild(booking_imageImg);
/* -------------------------------------------------------------------------------- */
        const booking_listDIV = document.createElement("div");
        booking_listDIV.className = "booking_list";

        const booking_attractionUl = document.createElement("ul");
        booking_attractionUl.className = "booking_attraction";
        const booking_attractionLi = document.createElement("li");
        booking_attractionLi.textContent = "台北一日遊：";
        const booking_attractionLi2 = document.createElement("li");
        booking_attractionLi2.textContent = e.attraction.name;
        booking_attractionUl.append(booking_attractionLi, booking_attractionLi2);

        const booking_dateUl = document.createElement("ul");
        booking_dateUl.className = "booking_date";
        const booking_list_itemLi_to_date = document.createElement("li");
        booking_list_itemLi_to_date.className = "booking_list_item";
        booking_list_itemLi_to_date.textContent = "日期：";
        const booking_dateLi = document.createElement("li");
        booking_dateLi.textContent = e.date;
        booking_dateUl.append(booking_list_itemLi_to_date, booking_dateLi);

        const booking_timeUl = document.createElement("ul");
        booking_timeUl.className = "booking_time";
        const booking_list_itemLi_to_time = document.createElement("li");
        booking_list_itemLi_to_time.className = "booking_list_item";
        booking_list_itemLi_to_time.textContent = "時間：";
        const booking_timeLi = document.createElement("li");
        if(e.time == "morning"){
            booking_timeLi.textContent = "早上9點 - 下午1點";
        };
        if(e.time == "afternoon"){
            booking_timeLi.textContent = "下午1點 - 下午6點";
        };
        booking_timeUl.append(booking_list_itemLi_to_time, booking_timeLi);

        const booking_priceUl = document.createElement("ul");
        booking_priceUl.className = "booking_price";
        const booking_list_itemLi_to_price = document.createElement("li");
        booking_list_itemLi_to_price.className = "booking_list_item";
        booking_list_itemLi_to_price.textContent = "費用：";
        const booking_priceLi = document.createElement("li");
        booking_priceLi.textContent = "新台幣" + e.price + "元";
        booking_priceUl.append(booking_list_itemLi_to_price, booking_priceLi);

        const booking_addressUl = document.createElement("ul")
        booking_addressUl.className = "booking_address"
        const booking_list_itemLi_to_address = document.createElement("li");
        booking_list_itemLi_to_address.className = "booking_list_item";
        booking_list_itemLi_to_address.textContent = "地點：";
        const booking_addressLi = document.createElement("li");
        booking_addressLi.textContent = e.attraction.address;
        booking_addressUl.append(booking_list_itemLi_to_address, booking_addressLi);
/* ------------------------------------------------------------------------------------ */
        const trashDIV = document.createElement("div");
        trashDIV.className = "trash";
        const delete_bookingImg = document.createElement("img");
        delete_bookingImg.className = "delete_booking";
        delete_bookingImg.setAttribute("booking_id", e.booking_id);
        delete_bookingImg.src = "/static/images/icon_delete.png";
        trashDIV.appendChild(delete_bookingImg);
/* ------------------------------------------------------------------------------------ */
        booking_listDIV.append(
            booking_attractionUl,
            booking_dateUl,
            booking_timeUl,
            booking_priceUl,
            booking_addressUl,
        )
        booking_overview_sectionDIV.append(
            booking_imageDIV,
            booking_listDIV,
            trashDIV,
        )
        booking_overall.append(
            booking_overview_sectionDIV,
        )

        ttl_price += e.price
        const booking_ttl_price = document.querySelector(".booking_ttl_price");
        booking_ttl_price.textContent = "總價：新台幣 " + ttl_price + " 元"
    })
}

/* ---------------------addEventListener delete image(trash) --------------------- */
document.addEventListener("click", function(e){
    const target = e.target.closest("[booking_id]");
    if(target){
        let bookingId = target.getAttribute('booking_id')
        delete_booking(bookingId)
    }
});

/* ---------------------------delete_booking function----------------------------- */
function delete_booking(bookingId){
    const url = "/api/booking"
    const headers = {
        "Content-Type": "application/json"
    };
    const body = {
       "booking_id": bookingId
    };
    fetch(url, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if(data.ok){
            location.reload()
        }
    })
}
    
/* ---------------------------------Automate User Data Imports-------------------- */
let userData = JSON.parse(sessionStorage.getItem("userData"))
const booking_subtitle = document.querySelector(".booking_subtitle");
booking_subtitle.textContent = "您好，" + userData.name + "，待預訂的行程如下：";

const booking_contact_name = document.getElementById("booking_contact_name");
booking_contact_name.value = userData.name;

const booking_contact_email = document.getElementById("booking_contact_email");
booking_contact_email.value = userData.email;

/* ---------------------------------Connect Cash Flow with TapPay-------------------- */
const APP_ID = 126926
const APP_KEY = "app_qMdNyqhTAkEsseMgGTa1oQXbf4tzRoxRXJAqnfdnYEKRSjKtOUai0IkoZhj3"
TPDirect.setupSDK(APP_ID, APP_KEY, 'sandbox')

let fields = {
    number: {
        element: '#card-number',
        placeholder: "**** **** **** ****"
    },
    expirationDate: {
        element: document.getElementById('card-expiration-date'),
        placeholder: "MM / YY"
    },
    ccv: {
        element: '#card-ccv',
        placeholder: "ccv"
    }
}
TPDirect.card.setup({
    fields: fields,
    styles: {
        'input': {
            'color': 'gray'
        },
        'input.card-number': {
            'font-size': '16px'
        },
        'input.ccv': {
            'font-size': '16px'
        },
        'input.expiration-date': {
            'font-size': '16px'
        },
        '.valid': {
            'color': 'green'
        },
        '.invalid': {
            'color': 'red'
        },
    },
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 4,
        endIndex: 11
    }
})


/* ---------------------------------confirm and payment-------------------- */
function getBookingData(bookingData){
    const orderAndPay = document.querySelector(".orderAndPay")
    orderAndPay.addEventListener("click", function(event){
        event.preventDefault()
        let contactName = document.querySelector("#booking_contact_name").value
        let contactEmail = document.querySelector("#booking_contact_email").value
        let contactPhoneNumber = document.querySelector("#booking_contact_phone").value

        if(contactName == "" | contactEmail == "" | contactPhoneNumber == ""){
            const booking_contact_phone = document.querySelector(".booking_contact_phone")
            const ErrorMessage = document.createElement("div")
            ErrorMessage.className = "errorMessage"
            ErrorMessage.textContent = "請確認欄位皆已輸入"
            booking_contact_phone.appendChild(ErrorMessage)
            return
        }
        const tappayStatus = TPDirect.card.getTappayFieldsStatus()
        if (tappayStatus.canGetPrime === false){
            const payment = document.querySelector(".payment")
            const ErrorMessage = document.createElement("div")
            ErrorMessage.className = "errorMessage"
            ErrorMessage.textContent = "信用卡資訊錯誤，或是請洽發卡銀行機構"
            payment.appendChild(ErrorMessage)
            return
        }
        TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                alert("發生錯誤：" + result.msg)
                return
            }

            let prime = result.card.prime
            let trip = []
            let totalPrice = 0
            for(let i = 0; i < bookingData.data.length; i++){
                let att = {
                    "attraction": {
                        "id": bookingData.data[i].attraction.id,
                        "name": bookingData.data[i].attraction.name,
                        "address": bookingData.data[i].attraction.address,
                        "image": bookingData.data[i].attraction.image
                      },
                      "date": bookingData.data[i].date,
                      "time": bookingData.data[i].time
                }
                trip.push(att)
                totalPrice += bookingData.data[i].price
            }

            const url = "/api/orders";
            const headers = {
                "Content-Type": "application/json"
            };
            let body = {
                "prime": prime,
                "order": {
                    "price": totalPrice,
                    "trip": trip
                },
                "contact":{
                    "name": contactName,
                    "email": contactEmail,
                    "phone": contactPhoneNumber
                }
            }

            fetch(url, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(body)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if(data.data.payment.message == "付款成功"){
                    window.location.href = "/thankyou?number=" + data.data.number
                }
                else{
                    const booking_confirm = document.querySelector(".booking_confirm");
                    const details = document.querySelector(".details");
                    const detailsDiv = document.createElement("div");
                    detailsDiv.className = "errorMessage";
                    detailsDiv.textContent = "付款失敗，請稍後再試或洽發卡銀行機構";
                    details.insertBefore(detailsDiv, booking_confirm)
                }
            })
        })  
    })
}


/*--------------------input addEventListener of remove error message--------------------*/
const bookingContactNameInput = document.getElementById("booking_contact_name")
bookingContactNameInput.addEventListener("click", function(){
    removeErrorMessage()
})
const bookingContactEmailInput = document.getElementById("booking_contact_email")
bookingContactEmailInput.addEventListener("click", function(){
    removeErrorMessage()
})

const bookingContactPhoneInput = document.getElementById("booking_contact_phone")
bookingContactPhoneInput.addEventListener("click", function(){
    removeErrorMessage()
})

const orderAndPay = document.querySelector(".orderAndPay")
orderAndPay.addEventListener("click", function(){
    removeErrorMessage()
})


/*--------------------function of remove error message--------------------*/
function removeErrorMessage(){
    const errorMessage = document.querySelector(".errorMessage")
    if(errorMessage){
        errorMessage.remove()
    }
}