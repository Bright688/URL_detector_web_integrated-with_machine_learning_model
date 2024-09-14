document.getElementById("urlForm").addEventListener("submit", function() {
    document.getElementById("loadingBox").style.display = "block";
    // Hide the result box while loading
    const resultBox = document.querySelector(".result-box");
    if (resultBox) {
         resultBox.style.display = "none";
    }
});