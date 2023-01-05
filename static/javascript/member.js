const fileUploader = document.querySelector("#file-uploader");

fileUploader.addEventListener("change", (e) => {
   console.log(e.target.files); 
});