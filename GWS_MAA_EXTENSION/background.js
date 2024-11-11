chrome.runtime.onInstalled.addListener(function() {
  console.log("GWS MAA Extension installed.");
});

chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.create({ url: chrome.extension.getURL('popup.html') });
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "auth") {
    chrome.identity.getAuthToken({ interactive: true }, function(token) {
      if (chrome.runtime.lastError || !token) {
        console.error(chrome.runtime.lastError);
        sendResponse({ success: false, error: chrome.runtime.lastError });
      } else {
        sendResponse({ success: true, token: token });
      }
    });
    return true; // Will respond asynchronously.
  }
});