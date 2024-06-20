// 변경하고자 하는 Thumbnail URL
const classification = 'http://127.0.0.1:8080/predict'
const change_thumbnail = 'https://img1.freepng.ru/20171221/vuq/blocked-png-clipart-5a3bff14f1dca9.6734700315138813649907.jpg'
let thumbnail_src_set = new Set()


// 비동기적으로 Thumbnail Src를 보내는 함수
async function replacethumbnail(thumbnail) {
  try{
    const response = await fetch(classification, {
      method: 'POST',
      body: JSON.stringify({ url: thumbnail.src}),
      headers: {
        'Content-Type' : 'application/json'
      }
    });
    const data = await response.json();

    // image의 Class가 혐오 Class인 경우 썸네일을 변경
    if (data.class == 'insect' || data.class == 'skin' || data.class == 'tryphopobia' || data.class == 'deadbody'){
        thumbnail.src = change_thumbnail;
    }
  } catch (error) {
    console.error("오류발생", error);
  }
}


function classification_thumbnail() {
  let thumbnails = document.querySelectorAll('#thumbnail > yt-image > img');
  thumbnails.forEach(thumbnail => {
    if(thumbnail.src != "" && !thumbnail_src_set.has(thumbnail.src)){
      thumbnail_src_set.add(thumbnail.src);
      console.log(thumbnail.src);
      replacethumbnail(thumbnail);
    }
  });
}

// 새로고침 or 페이지가 로딩이 된 후 수행

window.onload = function() {
  thumbnail_src_set.clear();
  classification_thumbnail();
  observer.disconnect();
  observer.observe(document.body, {childList:true, subtree: true});
};


// DOM의 변화를 감지하고 함수를 실행하는 Observer
const observer = new MutationObserver((mutation) => {
  classification_thumbnail();
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});

// 최초 실행하는 함수
classification_thumbnail();

// 현재 페이지에서 벗어날 경우 Thumbnail 집합을 초기화
window.addEventListener('beforeunload', function() {
  thumbnail_src_set.clear();
});






