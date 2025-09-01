const pageLoadTime = new Date().getTime();
sessionStorage.setItem("pageLoadTime", pageLoadTime);

$("#nextButton").click(function (event) {
  var timeLimit = 10;
  var earlyClickCount = 0;
  var clickTime = new Date().getTime();
  var pageLoadTime = sessionStorage.getItem("pageLoadTime");
  var timeDifference = (clickTime - pageLoadTime) / 1000;
  if (timeDifference < timeLimit) {
    event.preventDefault();
    alert("Please carefully study the information provided before continuing");
    earlyClickCount++;
    document.getElementById("EarlyClickCount").value = earlyClickCount;
  }
});
