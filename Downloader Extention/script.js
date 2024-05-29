document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('videoDownload').addEventListener('click', () => {
        chrome.runtime.sendMessage({ message: "callgetVideoApi" }, (response) => {
            if (response && response.success) {
                console.log("Api request successful");
            } else {
                console.error("Error in API request");
            }
        });
    });

    document.getElementById('addUrl').addEventListener('click', () => {
        chrome.runtime.sendMessage({ message: "calladdUrlApi" }, (response) => {
            if (response && response.success) {
                console.log("Api request successful");
            } else {
                console.error("Error in API request");
            }
        });
    });
    
    document.getElementById('downloadqueue').addEventListener('click', () => {
        chrome.runtime.sendMessage({ message: "callDownloadQueue" }, (response) => {
            if (response && response.success) {
                console.log("Api request successful");
            } else {
                console.error("Error in API request");
            }
        });
    });
});
