let nextPage = 0;
let nextPageAndKeyword = false
//loading default content
window.onload = async function(){ 
    await fetch("/api/attractions?page=" + nextPage)
    .then(res => res.json())
    .then(data => {
        for(let i = 0; i < data.data.length; i++){
            const spotImage = document.querySelectorAll(".spotImage");
            const spotImageDiv = document.createElement("img");
            spotImageDiv.src = data.data[i].images[0];
            spotImage[i].appendChild(spotImageDiv);

            const spotName = document.querySelectorAll(".tag");
            const spotNameDiv = document.createElement("div");
            spotNameDiv.textContent = data.data[i].name;
            spotNameDiv.className = "spot";
            spotName[i].appendChild(spotNameDiv);

            const spotMRT = document.querySelectorAll(".information");
            const spotMRTDiv = document.createElement("div");
            spotMRTDiv.textContent = data.data[i].mrt;
            spotMRTDiv.className = "mrt";
            spotMRT[i].appendChild(spotMRTDiv);

            const spotCategory = document.querySelectorAll(".information");
            const spotCategoryDiv = document.createElement("div");
            spotCategoryDiv.textContent = data.data[i].category;
            spotCategoryDiv.className = "category";
            spotCategory[i].appendChild(spotCategoryDiv);
        }
        nextPage = data.nextPage;
    })
    await fetch("/api/categories")
    .then(res => res.json())
    .then(menu =>{
        for(i = 0; i < menu.data.length; i++){
            const menuCategory = document.querySelector(".menu-category");
            const menuCategoryDiv = document.createElement("span");
            menuCategoryDiv.textContent = menu.data[i];
            menuCategoryDiv.className = "menu-item";
            menuCategory.appendChild(menuCategoryDiv);
        }
    })
    const menu = document.querySelectorAll(".menu-item");
    menu.forEach(element =>{
        element.addEventListener("click", function(e){
            result = e.target.innerText;
            document.querySelector(".search-bar").value = result;
        })
    })
}



//searching
let func = {
    fetchData: function(keyword){
        const container = document.querySelector(".container");
        if(!keyword){
            url = "/api/attractions?page=" + nextPage
        }
        if(keyword){
            if(nextPageAndKeyword == true){
                url = "/api/attractions?page=" + nextPage + "&keyword=" + keyword
            }
            else{
                nextPage = 0
                url = "/api/attractions?page=" + nextPage + "&keyword=" + keyword
            }
        }
        fetch(url)
        .then((res) => {
            return res.json();
        }).then(data => {
            if(data.data[0] === undefined){ //Not found data
                observer.unobserve(target);
                while(container.firstChild){
                    container.removeChild(container.firstChild);   
                }
                const newCard = document.createElement("div");
                const textNode = document.createTextNode("很抱歉，查無相關資料！");
                newCard.appendChild(textNode);
                newCard.style.color = 'red';
                container.appendChild(newCard);
            }
            else{
                if(keyword && nextPage == 0){
                    while(container.firstChild){
                    container.removeChild(container.firstChild);   
                    }
                }
                for(let i = 0; i < data.data.length; i++){
                    const newCard = document.createElement("article");
                    newCard.className = "card";
                    const newSpotImage = document.createElement("div");
                    newSpotImage.className = "spotImage";
                    const newTag = document.createElement("div");
                    newTag.className = "tag";
                    const newInformation = document.createElement("div");
                    newInformation.className = "information";
                    newCard.append(newSpotImage, newTag, newInformation);
        
                    const spotImageDiv = document.createElement("img");
                    spotImageDiv.src = data.data[i].images[0];
                    newSpotImage.appendChild(spotImageDiv);
                    
                    const spotNameDiv = document.createElement("div");
                    spotNameDiv.className = "spot";
                    spotNameDiv.textContent = data.data[i].name;
                    newTag.appendChild(spotNameDiv);
                    
                    const spotMRTDiv = document.createElement("div");
                    spotMRTDiv.className = "mrt";
                    spotMRTDiv.textContent = data.data[i].mrt;
        
                    const spotCategoryDiv = document.createElement("div");
                    spotCategoryDiv.className = "category";
                    spotCategoryDiv.textContent = data.data[i].category;
                    newInformation.append(spotMRTDiv, spotCategoryDiv);
                    
                    container.appendChild(newCard);
                }
            }
            nextPage = data.nextPage;
            if(nextPage != null && keyword){
                nextPageAndKeyword = true
            }
            else if(nextPage == null){
                nextPageAndKeyword = false
            }
        })
    },
    search: function(){
        keyword = document.querySelector(".search-bar").value
        if(keyword){
            this.fetchData(keyword)
        }
    }
}
document
    .querySelector(".search button")
    .addEventListener("click", function(){
        func.search();
    });

document
    .querySelector(".search-bar")
    .addEventListener("keyup", function(event){
        if (event.key == "Enter"){
            func.search();
        }
    });


//創造 Intersection Observer物件
const observer = new IntersectionObserver(
function (entries){
    // 每當目標元素(footer)進入畫面後就呼叫函式
    if(nextPage === null){
        return;
    }
    if(entries[0].isIntersecting && nextPageAndKeyword == true){
        func.fetchData(keyword); 
    }
    if(entries[0].isIntersecting && nextPageAndKeyword == false){
        func.fetchData();      
    }
},{rootMargin: '0px',
    threshold: 1,}
);

//綁定欲觀察的target
const target = document.querySelector("footer");
observer.observe(target);
