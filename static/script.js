
const scanForm = document.getElementById("scanForm");
const scanButton = document.getElementById("scanButton");
const loadingMessage = document.getElementById("loadingMessage");
const websiteUrl = document.getElementById("websiteUrl");

scanForm.addEventListener("submit", function(event) {

    const url = websiteUrl.value.trim();

    if (url.length === 0) {
        event.preventDefault();
        alert("Please enter a website URL.");
        return;
    }

    scanButton.disabled = true;
    scanButton.textContent = "Scanning...";

    loadingMessage.hidden = false;

});

// Reset button when page loads or is restored
window.addEventListener("pageshow", function() {

    scanButton.disabled = false;
    scanButton.textContent = "Scan Website";

    loadingMessage.hidden = true;

});
