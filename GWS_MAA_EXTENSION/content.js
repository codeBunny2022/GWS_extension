// Basic content script to interact with the web page
console.log("GWS MAA Content Script Loaded");

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  // Handling the interaction with the web page if necessary
  if (request.action === "doSomething") {
    console.log("Doing something on the webpage.");
    sendResponse({ success: true });
  }
});