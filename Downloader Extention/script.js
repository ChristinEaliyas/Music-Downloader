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

    document.getElementById('Music').addEventListener('click', () =>{
        chrome.runtime.sendMessage({ message: "ChangeDirectory", name: 'Music'}, (response) => {
            if (response && response.success) {
                console.log("Api request successful");
            } else {
                console.error("Error in API request");
            }
        });
    })
    document.getElementById('Malayalam').addEventListener('click', () =>{
        chrome.runtime.sendMessage({ message: "ChangeDirectory", name: 'Malayalam'}, (response) => {
            if (response && response.success) {
                console.log("Api request successful");
            } else {
                console.error("Error in API request");
            }
        });
    })
    document.getElementById('Devotional').addEventListener('click', () =>{
        chrome.runtime.sendMessage({ message: "ChangeDirectory", name: 'Devotional'}, (response) => {
            if (response && response.success) {
                console.log("Api request successful");
            } else {
                console.error("Error in API request");
            }
        });
    })

    document.getElementById('folderSelect').addEventListener('click', () => {
        document.getElementById('dropdown-content').style.display = 'block';
        document.getElementById('video-section').style.display = 'none'

        setTimeout(() => {
            document.getElementById('dropdown-content').style.display = 'none';
            document.getElementById('video-section').style.display = 'block'

        }, 5000);
    })
});


