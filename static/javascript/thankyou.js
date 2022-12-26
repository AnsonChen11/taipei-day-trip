let url = window.location.href;
let orderNumber = url.split("=")[1];


fetchOrderNumberAPI()

function fetchOrderNumberAPI(){
    fetch("/api/order/" + orderNumber)
    .then(response => response.json())
    .then(data => {
        if(data.message == "未登入系統"){
            location.href="/";
        }
        else{
            createElementForThankyou(data)
        }
    })
}



/* ---------------create Thankyou and details ---------------- */
function createElementForThankyou(data){
    const thankyou_overall = document.querySelector(".thankyou_overall");
/* -------------------------------------------------------------------------------- */    
    let userData = JSON.parse(sessionStorage.getItem("userData"))

    const thankyou_subtitle = document.querySelector(".thankyou_subtitle")
    thankyou_subtitle.textContent = userData.name + "感謝您的預定！您的訂單資訊如下："

    const thankyou_orderNumber = document.querySelector(".thankyou_orderNumber")
    thankyou_orderNumber.textContent = "訂單編號：" + data.data.number

    const thankyou_orderName = document.querySelector(".thankyou_orderName")
    thankyou_orderName.textContent = "聯絡姓名：" + data.data.contact.name

    const thankyou_contactPhone = document.querySelector(".thankyou_contactPhone")
    thankyou_contactPhone.textContent = "聯絡電話：" + data.data.contact.phone

    const thankyou_contactEmail = document.querySelector(".thankyou_contactEmail")
    thankyou_contactEmail.textContent = "聯絡信箱：" + data.data.contact.email

    const thankyou_totalPrice = document.querySelector(".thankyou_totalPrice")
    thankyou_totalPrice.textContent = "訂單金額：" + data.data.totalPrice

/* -------------------------------------------------------------------------------- */
    data.data.trip.forEach((e) =>{
        const thankyou_overview_sectionDIV = document.createElement("div");
        thankyou_overview_sectionDIV.className = "thankyou_overview_section"
/* -------------------------------------------------------------------------------- */
        const thankyou_imageDIV = document.createElement("div");
        thankyou_imageDIV.className = "thankyou_image";
        const thankyou_imageImg = document.createElement("img");
        thankyou_imageImg.src = e.attraction.image;
        thankyou_imageDIV.appendChild(thankyou_imageImg);
/* -------------------------------------------------------------------------------- */
        const thankyou_listDIV = document.createElement("div");
        thankyou_listDIV.className = "thankyou_list";

        const thankyou_attractionUl = document.createElement("ul");
        thankyou_attractionUl.className = "thankyou_attraction";
        const thankyou_attractionLi = document.createElement("li");
        thankyou_attractionLi.textContent = "台北一日遊：";
        const thankyou_attractionLi2 = document.createElement("li");
        thankyou_attractionLi2.textContent = e.attraction.name;
        thankyou_attractionUl.append(thankyou_attractionLi, thankyou_attractionLi2);

        const thankyou_dateUl = document.createElement("ul");
        thankyou_dateUl.className = "thankyou_date";
        const thankyou_list_itemLi_to_date = document.createElement("li");
        thankyou_list_itemLi_to_date.className = "thankyou_list_item";
        thankyou_list_itemLi_to_date.textContent = "日期：";
        const thankyou_dateLi = document.createElement("li");
        thankyou_dateLi.textContent = e.date;
        thankyou_dateUl.append(thankyou_list_itemLi_to_date, thankyou_dateLi);

        const thankyou_timeUl = document.createElement("ul");
        thankyou_timeUl.className = "thankyou_time";
        const thankyou_list_itemLi_to_time = document.createElement("li");
        thankyou_list_itemLi_to_time.className = "thankyou_list_item";
        thankyou_list_itemLi_to_time.textContent = "時間：";
        const thankyou_timeLi = document.createElement("li");
        if(e.time == "morning"){
            thankyou_timeLi.textContent = "早上9點 - 下午1點";
        };
        if(e.time == "afternoon"){
            thankyou_timeLi.textContent = "下午1點 - 下午6點";
        };
        thankyou_timeUl.append(thankyou_list_itemLi_to_time, thankyou_timeLi);

        const thankyou_priceUl = document.createElement("ul");
        thankyou_priceUl.className = "thankyou_price";
        const thankyou_list_itemLi_to_price = document.createElement("li");
        thankyou_list_itemLi_to_price.className = "thankyou_list_item";
        thankyou_list_itemLi_to_price.textContent = "費用：";
        const thankyou_priceLi = document.createElement("li");
        thankyou_priceLi.textContent = "新台幣" + e.price + "元";
        thankyou_priceUl.append(thankyou_list_itemLi_to_price, thankyou_priceLi);

        const thankyou_addressUl = document.createElement("ul")
        thankyou_addressUl.className = "thankyou_address"
        const thankyou_list_itemLi_to_address = document.createElement("li");
        thankyou_list_itemLi_to_address.className = "thankyou_list_item";
        thankyou_list_itemLi_to_address.textContent = "地點：";
        const thankyou_addressLi = document.createElement("li");
        thankyou_addressLi.textContent = e.attraction.address;
        thankyou_addressUl.append(thankyou_list_itemLi_to_address, thankyou_addressLi);
/* ------------------------------------------------------------------------------------ */
        thankyou_listDIV.append(
            thankyou_attractionUl,
            thankyou_dateUl,
            thankyou_timeUl,
            thankyou_priceUl,
            thankyou_addressUl,
        )
        thankyou_overview_sectionDIV.append(
            thankyou_imageDIV,
            thankyou_listDIV,
        )
        thankyou_overall.append(
            thankyou_overview_sectionDIV,
        )
    })
}