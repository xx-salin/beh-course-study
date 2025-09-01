var clickCount = 0;
var timeStampData = [];

function recordButtonClick() {
  clickCount += 1;
  document.getElementById("moreInfoClickCount").value = clickCount;
  var openTimestamp = new Date().toISOString();
  timeStampData.push("Opened: " + openTimestamp);
  updateTimeStampField();
}

$("#moreInfoModal").on("hidden.bs.modal", function () {
  var closeTimestamp = new Date().toISOString();
  timeStampData.push("Closed: " + closeTimestamp);
  updateTimeStampField();
});

function updateTimeStampField() {
  document.getElementById("timeStampMoreInfo").value = timeStampData.join("; ");
}
