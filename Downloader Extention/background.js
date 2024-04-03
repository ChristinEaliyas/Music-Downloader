const postUrl = "http://127.0.0.1:9000/api/music";

chrome.commands.onCommand.addListener(function (command) {
  if (command === "executeFunction") {
    chrome.tabs.query({}, function (tabs) {
      let youtubeTab = tabs.find(tab => tab.url.includes("youtube.com"));
      console.log(youtubeTab)
      // var tab = tabs[0];
      var data = JSON.stringify({ url: String(youtubeTab.url) });

      const requestOptions = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: data,
      };

      fetch(postUrl, requestOptions)
        .then((response) => {
          if (!response.ok) {
            console.log("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          // Handle successful response
          console.log("Success:", data);
        })
        .catch((error) => {
          console.error("Fetch error:", error);
        });
    });
  }
});
