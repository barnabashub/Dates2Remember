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
