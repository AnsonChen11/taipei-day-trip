const fileUploader = document.querySelector("#file-uploader");


fileUploader.addEventListener("change", (e) => {
   let file = e.target.files[0];
   let formData = new FormData();
   formData.append("file", file);

   fetch("/upload", {
      method: "POST",
      body: formData,
   })
  .then(response => response.json())
  .then(data => {
      console.log(data)
  })
});



const profileHistoryOrders = document.querySelector(".profile_history_orders");
profileHistoryOrders.addEventListener("click", function(){
   location.href = "/historyOrders";
})