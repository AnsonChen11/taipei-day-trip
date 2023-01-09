fetchApiMember()

function fetchApiMember(){
   let userData = JSON.parse(sessionStorage.getItem("userData"));
   const profile_name = document.querySelector(".profile_name");
   profile_name.textContent = userData.name;

   // let profilePicURL = sessionStorage.getItem("profile_pic");
   // const profilePic = document.querySelector(".profile_pic")
   // profilePic.src = profilePicURL;
   fetch("/member")
   .then(response => response.json())
   .then(data => {
      if(data.message === "未登入系統"){
         location.href="/";
         return
      }
   })
}


const fileUploader = document.querySelector("#file-uploader");
fileUploader.addEventListener("change", (e) => {
   let file = e.target.files[0];
   if(file){
      const profilePic = document.querySelector(".profile_pic")
      profilePic.src = URL.createObjectURL(file)
   }
   let formData = new FormData();
   formData.append("file", file);

//    fetch("/upload", {
//       method: "POST",
//       body: formData,
//    })
//   .then(response => response.json())
//   .then(data => {
//       let profilePicURL = "data:image/jpg;base64," + data.image_url;
//       const profilePic = document.querySelector(".profile_pic")
//       profilePic.src = profilePicURL;

//       sessionStorage.setItem("profile_pic", profilePicURL)
//   })
});


const profileHistoryOrders = document.querySelector(".profile_history_orders");
profileHistoryOrders.addEventListener("click", function(){
   location.href = "/historyOrders";
})