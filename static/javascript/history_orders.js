fetchApiOrders()

function fetchApiOrders(){
    let userData = JSON.parse(sessionStorage.getItem("userData",));
    let user_id = userData.id;
    fetch("/api/orders/" + user_id)
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if(data.message === "未登入系統"){
            location.href="/";
            return
        }
        if(data.data === null){
            createElementForNoHistoryOrders()
            return
        }
        createElementForHistoryOrders(data);
    })
}

function createElementForHistoryOrders(data){
    const main = document.querySelector("main");
/* -------------------------------------------------------------------------------- */    
    let userData = JSON.parse(sessionStorage.getItem("userData"));

    const history_view = document.querySelector(".history_view");
    const history_viewH2 = document.createElement("h2");
    history_viewH2.textContent = userData.name + "！您的訂單紀錄如下：";
    history_view.appendChild(history_viewH2);
/* -------------------------------------------------------------------------------- */
    data.data.forEach((e) =>{
        const article = document.createElement("article");
        const containerDiv = document.createElement("div");
        containerDiv.className = "container";
        const ordersNumberDiv = document.createElement("div");
        ordersNumberDiv.className = "orders_number orders_date";
        const ordersNumberH3 = document.createElement("h3");
        ordersNumberH3.textContent = "訂單編號：" + e.number;
        const ordersDateH3 = document.createElement("h3");
        ordersDateH3.textContent = convertDateFormat(e.order_time);
        ordersNumberDiv.append(ordersNumberH3, ordersDateH3);
/* -------------------------------------------------------------------------------- */
        const ordersOverallDiv = document.createElement("div");
        ordersOverallDiv.className = "orders_overall";
        const ordersOverallDetailsDiv = document.createElement("div");
        ordersOverallDetailsDiv.className = "orders_overall_details";
        const ordersTitleH4 = document.createElement("h4");
        e.trip.length >= 2 ? 
        (attractionName = e.trip[0].attraction.name + "、" + e.trip[1].attraction.name + "...等"):
        (attractionName = e.trip[0].attraction.name)
        ordersTitleH4.textContent = "台北一日遊："+ attractionName;
        const ordersTotalPriceH4 = document.createElement("h4");
        ordersTotalPriceH4.textContent = "訂購總額：NT$" + e.totalPrice;
        const ordersStatusH4 = document.createElement("h4");
        ordersStatusH4.className = "orders_status";
        e.status === 0 ? (ordersStatusH4.textContent = "已確認訂單"):(ordersStatusH4.textContent = "訂單未確認");
        const ordersDetailsButton = document.createElement("button");
        ordersDetailsButton.className = "orders_details_button";
        const ordersDetailsA = document.createElement("a");
        ordersDetailsA.href = "/thankyou?number=" + e.number;
        ordersDetailsA.textContent = "訂購明細"
        ordersDetailsButton.appendChild(ordersDetailsA)
        ordersOverallDetailsDiv.append(ordersTitleH4, ordersTotalPriceH4, ordersStatusH4, ordersDetailsButton)
        const ordersImgDiv = document.createElement("div"); 
        ordersImgDiv.className = "orders_img";
        const ordersImg = document.createElement("img"); 
        ordersImg.src = e.trip[0].attraction.image
        ordersImgDiv.appendChild(ordersImg)
        ordersOverallDiv.append(ordersOverallDetailsDiv, ordersImgDiv)
/* ------------------------------------------------------------------------------------ */
        containerDiv.append(
            ordersNumberDiv,
            ordersOverallDiv,
        )
        article.appendChild(
            containerDiv,
        )
        main.appendChild(
            article,
        )
    })
}


function createElementForNoHistoryOrders(){
/* -------------------------------------------------------------------------------- */    
    let userData = JSON.parse(sessionStorage.getItem("userData"));
    const history_view = document.querySelector(".history_view");
    const history_viewH2 = document.createElement("h2");
    history_viewH2.textContent = userData.name + "！您目前沒有任何訂單！";
    history_view.appendChild(history_viewH2);
}


function convertDateFormat(data) {
    const options = {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
      timeZone: "GMT",
    };
    const dateString = data.replace("GMT", "UTC");
    const date = new Date(dateString);
    const formattedTime = new Intl.DateTimeFormat("ko-KR", options).format(date);
    return formattedTime;
  }
  
