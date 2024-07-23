function sendRequest() {
  const userInput = document.getElementById("userInput").value;
  const url = `/api/get_when_will?day=${userInput}&date=2021-09-01`;
  if (userInput == "") {
    document.getElementById("userInput").placeholder = "Please enter a number";
    document.getElementById("response").textContent = "";
    return;
  } else {
    fetch(url)
      .then((response) => response.text())
      .then((data) => {
        document.getElementById("response").textContent = data;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

function onAfterInit() {
  const date = document.getElementById("datedate").textContent;
  const daysapiurl = `/api/${date}/get_howold_indays`;
  fetch(daysapiurl)
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("daysagotext").textContent = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  const monthapiurl = `/api/${date}/get_howold_inmonths`;
  fetch(monthapiurl)
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("monthagotext").textContent = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

window.onload = onAfterInit;
