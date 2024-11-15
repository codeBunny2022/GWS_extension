document.getElementById("login").addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "authenticate" }, (response) => {
        if (response.token) {
          alert("Authenticated Successfully!");
        } else {
          alert("Authentication Failed!");
        }
      });
    });

    document.getElementById("start-task").addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "authenticate" }, (response) => {
        if (response.token) {
          // Make a request to the Flask server with the obtained token
          const requestData = {
            task: "create_spreadsheet",
            already_done: "",
            workspace_content: "",
            prompt_history: "",
            current_service_url: "",
            service_history: "",
            token: response.token
          };

          fetch("http://localhost:5000/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
          })
          .then(response => response.json())
          .then(data => {
            document.getElementById("response").innerText = JSON.stringify(data);
          })
          .catch(error => {
            document.getElementById("response").innerText = error.message;
            console.error("Error:", error);
          });
        } else {
          alert("Authentication Failed!");
        }
      });
    });