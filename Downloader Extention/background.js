const musicApi = "http://127.0.0.1:9000/api/music";
const videoApi = "http://127.0.0.1:9000/api/video";
const saveUrlApi = "http://127.0.0.1:9000/api/addToList";
const downloadQueueApi = "http://127.0.0.1:9000/api/downloadQueue"
const ChangeDirecotyApi = "http://127.0.0.1:9000/api/changeDirecotory"

// Return the url of the first youtube tab.
async function geturl() {
  const tabs = await new Promise((resolve) => {
    chrome.tabs.query({}, resolve);
  });

  const youtubeTab = tabs.find((tab) => tab.url.includes("youtube.com"));
  console.log(youtubeTab);
  return JSON.stringify({ url: String(youtubeTab.url) });
}

// ---- Send Api Request -----
function postRequest(Api, requestOptions){
  fetch(Api, requestOptions)
  .then((response) => {
    if (!response.ok) {
      console.log("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    console.log("Success:", data);
    sendNotification(data)
  })
  .catch((error) => {
    console.error("Fetch error:", error);
  });
}

function sendNotification(data) {
  chrome.notifications.create({
    title: 'YouTube Downloader',
    message: JSON.stringify(data),
    iconUrl: 'images/logo128.png',
    type: 'basic'
  });
}

// ----- Video Downloader Api -----
async function getVideoApi() {
  const data = await geturl()

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: data,
  };

  postRequest(videoApi, requestOptions)
}

// ----- Add Url to a list -----
async function addUrlApi() {
  const data = await geturl()

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: data,
  };

  postRequest(saveUrlApi, requestOptions)
}

// ----- Download Queue -----
function downloadQueue(){
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: "Download The Queue"
  };

  postRequest(downloadQueueApi, requestOptions)
}

// ----- Change Directory -----
function ChangeDirecoty(Directory) {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ Directory }),
  };

  postRequest(ChangeDirecotyApi, requestOptions)

}

// ----- Audio Downloader Api -----
chrome.commands.onCommand.addListener(async function (command) {
  if (command === "executeFunction") {
    const data = await geturl()

    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: data,
    };

    postRequest(musicApi, requestOptions)
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === "callgetVideoApi") {
    getVideoApi();
    sendResponse({ success: true });
  }else if(request.message === "calladdUrlApi") {
    addUrlApi();
    sendResponse({ success:true });
  }else if(request.message === "callDownloadQueue") {
    downloadQueue()
    sendResponse({ success:true });
  }else if(request.message === "ChangeDirectory"){
    ChangeDirecoty(request.name)
    sendResponse({ success:true });
  }
});