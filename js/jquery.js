function postData(url, data) {
  // Default options are marked with *
  return fetch(url, {
    body: JSON.stringify(data), // must match 'Content-Type' header
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, same-origin, *omit
    headers: {
      'user-agent': 'Mozilla/4.0 MDN Example',
      'content-type': 'application/json'
    },
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, cors, *same-origin
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // *client, no-referrer
  })
  .then(response => response.json()) // 輸出成 json
}

function submit(){
  const keyin = document.getElementById('keyin').value;
  
  const data = {
    keyin
  }
  
  postData('https://wanjhen.github.io/poetryai/', data)
  .then(data=>{
    const result = data.result;
    console.log(result);
    document.getElementById('resultText').innerHTML=result;
  })
}

var swiper = new Swiper('.mySwiper', {
    slidesPerView: 7,
    spaceBetween: 5,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
  });