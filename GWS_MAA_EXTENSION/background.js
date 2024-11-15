chrome.runtime.onInstalled.addListener(() => {
  console.log("GWS MAA Extension installed");
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "authenticate") {
    chrome.identity.getAuthToken({ interactive: true }, function(token) {
      if (chrome.runtime.lastError || !token) {
        console.error(chrome.runtime.lastError);
        sendResponse({ token: null });
      } else {
        sendResponse({ token });
      }
    });
    return true; // Indicates that the response is sent asynchronously
  }
});