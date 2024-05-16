document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('videoDownload').addEventListener('click', () => {
        chrome.runtime.sendMessage({ message: "callgetVideoApi" }, (response) => {
            if (response.success) {
                console.log("Api request successful");
            }
        });
    });

    document.getElementById('addUrl').addEventListener('click', () => {
        chrome.runtime.sendMessage({ message: "calladdUrlApi" }, (response) => {
            if (response.success) {
                console.log("Api request successful");
            }
        });
    });
    
    document.getElementById('downloadqueue').addEventListener('click', () => {
        chrome.runtime.sendMessage({ message: "callDownloadQueue" }, (response) => {
            if (response.success) {
                console.log("Api request successful");
            }
        });
    });
});
