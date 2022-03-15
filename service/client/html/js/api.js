const API_URL = "http://141.98.252.168:55533/api/v1/"

window.onload = () => {
  console.log("load");
  document.getElementById('search').addEventListener('click', search)
}


function search() {
  const srcTxt = document.getElementById('src').value
  const destTxt = document.getElementById('dest').value
  const outputDiv = document.getElementById('output')

  const postData = {
    src: srcTxt,
    dest: destTxt
  }
  const headers = {
    method: "POST",
    body: JSON.stringify(postData)
  }
  fetch(API_URL+"devLinkPages", headers)
    .then(response => response.json())
    .then((data) => {
        outputDiv.innerHTML = JSON.stringify(data)
    });
}