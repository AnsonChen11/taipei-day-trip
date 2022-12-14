let ttl_price = 0
document.title = "台北一日遊 | 我的預定"
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
        const noOrderDiv = document.createElement("div");
        noOrderDiv.className = "noOrderItem";
        noOrderDiv.textContent = "目前無任何預定";
        main.appendChild(noOrderDiv);
    }
    else{
        const booking_overall = document.querySelector(".booking_overall");
        data.data.forEach((e) =>{
            const booking_overview_sectionDIV = document.createElement("div");
            booking_overview_sectionDIV.className = "booking_overview_section"
/* ------------------------------------------------------------------------------------------ */
            const booking_imageDIV = document.createElement("div");
            booking_imageDIV.className = "booking_image";
            const booking_imageImg = document.createElement("img");
            booking_imageImg.src = e.attraction.image;
            booking_imageDIV.appendChild(booking_imageImg);
/* ------------------------------------------------------------------------------------------ */
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
/* ------------------------------------------------------------------------------------------ */
            const trashDIV = document.createElement("div");
            trashDIV.className = "trash";
            const delete_bookingImg = document.createElement("img");
            delete_bookingImg.className = "delete_booking";
            delete_bookingImg.setAttribute("id", e.booking_id);
            delete_bookingImg.src = "/static/images/icon_delete.png";
            trashDIV.appendChild(delete_bookingImg);
/* ------------------------------------------------------------------------------------------ */
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
})




fetch("/api/user/auth")
.then(response => response.json())
.then(data => {
    const booking_subtitle = document.querySelector(".booking_subtitle");
    booking_subtitle.textContent = "您好，" + data.data.name + "，待預訂的行程如下：";

    const booking_contact_name = document.getElementById("booking_contact_name");
    booking_contact_name.value = data.data.name;

    const booking_contact_email = document.getElementById("booking_contact_email");
    booking_contact_email.value = data.data.email;
})



document.addEventListener("click", function(e){
    const target = e.target.closest(".delete_booking");
    if(target){
        delete_booking(target.id)
    }
});

function delete_booking(booking_id){
    const url = "/api/booking"
    const headers = {
        "Content-Type": "application/json"
    };
    const body = {
       "booking_id": booking_id
    };
    fetch(url, {
        method: "DELETE",
        headers: headers,
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        location.reload()
    })
}
    

