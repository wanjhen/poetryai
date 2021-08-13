function postData(url, data) {
  return fetch(url, {
    body: JSON.stringify(data),
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
      "user-agent": "Example",
      "content-type": "application/json"
    },
    method: "POST",
    mode: "cors",
    redirect: "follow",
    referrer: "no-referrer",
  })
    .then(response => response.json())
}

function submit(){
  const keyin = document.getElementById("keyin").value;
  
  const data = {
    keyin
  }
  
  postData("https://wanjhen.github.io/poetryai/", data)
  .then(data=>{
    const result = data.result;
    //console.log(result);
    document.getElementById("resultText").innerHTML=result;
  })
}

var swiper = new Swiper(".mySwiper", {
    slidesPerView: 7,
    spaceBetween: 5,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });