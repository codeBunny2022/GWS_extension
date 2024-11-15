// OAuth2 Authentication Flow
function authenticate(callback) {
  chrome.identity.getAuthToken({ interactive: true }, function(token) {
    if (chrome.runtime.lastError || !token) {
      console.error(chrome.runtime.lastError);
      callback(null);
    } else {
      callback(token);
    }
  });
}

function removeCachedAuthToken(token, callback) {
  chrome.identity.removeCachedAuthToken({ token: token }, function() {
    callback();
  });
}