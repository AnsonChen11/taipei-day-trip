const fileUploader = document.querySelector("#file-uploader");

fileUploader.addEventListener("change", (e) => {
   console.log(e.target.files); 
});


const profileHistoryOrders = document.querySelector(".profile_history_orders");
profileHistoryOrders.addEventListener("click", function(){
   location.href="/historyOrders";
})